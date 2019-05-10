# coding: utf-8
from __future__ import unicode_literals
import sys
from datetime import datetime

from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt

from journal.views import log_addition, log_change, log_deletion

import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from plate.models import Plate


@login_required
def index(request):
    return render(request, 'plate/index.html')


@login_required
def add(request):
    return render(request, 'plate/add.html')


@login_required
def edit(request, sid):
    plate = Plate.objects.get(pk=sid)
    return render(request, 'plate/edit.html', {'plate': plate})


@login_required
def detail(request, sid):
    plate = get_object_or_404(Plate, pk=sid)
    return render(request, 'plate/detail.html', {'plate': plate})


@login_required
def plate_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        plate_list = Plate.objects.filter(name__contains=key).order_by('-create_time').all()
    else:
        plate_list = Plate.objects.order_by('-create_time').all()
    paginator = Paginator(plate_list, limit)
    try:
        plates = paginator.page(page)
    except PageNotAnInteger:
        plates = paginator.page(1)
    except EmptyPage:
        plates = paginator.page(paginator.num_pages)
    for p in plates:
        tmp = dict()
        tmp['id'] = p.id
        tmp['name'] = p.name
        tmp['prefix'] = p.prefix
        tmp['icon'] = p.icon
        tmp['hits'] = p.hits
        tmp['stick'] = p.stick
        tmp['summary'] = p.summary
        tmp['update_time'] = str(p.update_time)
        if p.status == 1:
            staus_str = '已开启'
        elif p.status == 0:
            staus_str = '已关闭'
        else:
            p.status == 0
            staus_str = '已删除'
        tmp['status'] = staus_str
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(plate_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def insert(request):
    data = dict()
    status = False
    name = str(request.POST['name'])
    prefix = str(request.POST['prefix'])
    summary = str(request.POST['summary'])
    icon = str(request.POST['icon'])
    note = str(request.POST['note'])
    stick = True if str(request.POST['stick']) == 'true' else False
    plate = Plate(name=name, prefix=prefix, summary=summary, icon=icon, note=note, stick=stick)
    tmp_plate = Plate.objects.filter(name=name)
    if tmp_plate:
        msg = '添加失败, %s 已存在。' % name
    else:
        try:
            plate.save()
            msg = '添加成功'
            status = True
        except Exception as e:
            msg = e
        log_addition(request, plate, msg)
    data['msg'] = msg
    data['status'] = status
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def update(request):
    data = dict()
    status = False
    sid = int(request.POST['sid'])
    name = str(request.POST['name'])
    prefix = str(request.POST['prefix'])
    summary = str(request.POST['summary'])
    icon = str(request.POST['icon'])
    note = str(request.POST['note'])
    stick = True if str(request.POST['stick']) == 'true' else False
    p = Plate.objects.get(pk=sid)
    try:
        Plate.objects.filter(pk=sid).update(name=name, prefix=prefix, summary=summary, icon=icon, note=note,
                                            stick=stick)
        msg = '修改成功'
        status = True
    except Exception as e:
        msg = e.message
    log_change(request, p, msg)
    data['msg'] = msg
    data['status'] = status
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = Plate.objects.filter(pk__in=sids).all()
    for d_p in del_list:
        log = log_deletion(request, d_p, msg)
        try:
            Plate.objects.filter(pk=d_p.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e.message)
            msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")
