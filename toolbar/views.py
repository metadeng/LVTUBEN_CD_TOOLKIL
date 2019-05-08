# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from journal.views import log_addition, log_change, log_deletion


import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from plate.models import Plate
from toolbar.models import Toolbar


@login_required
def index(request):
    return render(request, 'toolbar/index.html')


@login_required
def add(request):
    plates = Plate.objects.filter(status__gte=0).all()
    return render(request, 'toolbar/add.html', {'plates': plates})


@login_required
def edit(request, sid):
    toolbar = Toolbar.objects.get(pk=sid)
    plates = Plate.objects.filter(status__gte=0).all()
    return render(request, 'toolbar/edit.html', {'toolbar': toolbar, 'plates': plates})


@login_required
def detail(request, sid):
    toolbar = get_object_or_404(Toolbar, pk=sid)
    return render(request, 'toolbar/detail.html', {'toolbar': toolbar})


@login_required
@csrf_exempt
def insert(request):
    data = dict()
    status = False
    name = str(request.POST['name'])
    plate_id = int(request.POST['plate']) if request.POST['plate'] else None
    alias = str(request.POST['alias'])
    title = str(request.POST['title'])
    note = str(request.POST['note'])
    icon = str(request.POST['icon'])
    color = str(request.POST['color'])
    avatar = str(request.POST['avatar'])
    server = str(request.POST['server'])
    port = int(request.POST['port']) if request.POST['port'] else 80
    file = request.FILES.get('file')
    stick = True if str(request.POST['stick']) == 'true' else False
    https = True if str(request.POST['https']) == 'true' else False
    plate = Plate.objects.get(pk=plate_id)
    toolbar = Toolbar(name=name, alias=alias, title=title, color=color, icon=icon, server=server,
                      port=port, https=https, avatar=file,
                      stick=stick, note=note)
    if plate:
        toolbar.plate = plate
        try:
            toolbar.save()
            status = True
            msg = '添加成功'
        except Exception as e:
            print(e.message)
            msg = e.message
    else:
        msg = '未查询到对应导航'
    log_addition(request, toolbar, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def update(request):
    data = dict()
    status = False
    sid = int(request.POST['sid'])
    name = str(request.POST['name'])
    plate_id = int(request.POST['plate']) if request.POST['plate'] else None
    alias = str(request.POST['alias'])
    title = str(request.POST['title'])
    note = str(request.POST['note'])
    icon = str(request.POST['icon'])
    color = str(request.POST['color'])
    avatar = str(request.POST['avatar'])
    server = str(request.POST['server'])
    port = int(request.POST['port']) if request.POST['port'] else 80
    file = request.FILES.get('file')
    stick = True if str(request.POST['stick']) == 'true' else False
    https = True if str(request.POST['https']) == 'true' else False
    plate = Plate.objects.get(pk=plate_id)
    if sid:
        toolbar = Toolbar.objects.get(pk=sid)
        try:
            Toolbar.objects.filter(pk=sid).update(name=name, plate=plate, alias=alias, title=title, note=note,
                                                  icon=icon, color=color, avatar=file, server=server,
                                                  port=port,
                                                  stick=stick, https=https)
            status = True
            msg = '修改成功'
        except Exception as e:
            print(e.message)
            msg = e.message
        log_change(request, toolbar, msg)
    else:
        msg = '未查询到相应工具'
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def toolbar_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        toolbar_list = Toolbar.objects.filter(name__contains=key).order_by('-create_time').all()
    else:
        toolbar_list = Toolbar.objects.order_by('-create_time').all()
    paginator = Paginator(toolbar_list, limit)
    try:
        toolbars = paginator.page(page)
    except PageNotAnInteger:
        toolbars = paginator.page(1)
    except EmptyPage:
        toolbars = paginator.page(paginator.num_pages)
    for t in toolbars:
        tmp = dict()
        tmp['id'] = t.id
        tmp['name'] = t.name
        tmp['alias'] = t.alias
        tmp['title'] = t.title
        tmp['icon'] = t.icon
        tmp['avatar'] = str(t.avatar)
        tmp['note'] = t.note
        tmp['hits'] = t.hits
        tmp['stick'] = t.stick
        tmp['server'] = t.server
        tmp['port'] = t.port
        tmp['plate'] = t.plate.name
        tmp['update_time'] = str(t.update_time)
        if t.status == 1:
            status_str = '已开启'
        elif t.status == 0:
            status_str = '已关闭'
        else:
            status_str = '已删除'
        tmp['status'] = status_str
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(toolbar_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = Toolbar.objects.filter(pk__in=sids).all()
    for d_t in del_list:
        log = log_deletion(request, d_t, msg)
        try:
            Toolbar.objects.filter(pk=d_t.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e.message)
            msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")
