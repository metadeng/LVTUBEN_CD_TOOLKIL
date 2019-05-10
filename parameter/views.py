# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from journal.views import log_deletion, log_addition, log_change
from parameter.models import Parameter


@login_required
def index(request):
    return render(request, 'parameter/index.html')


@login_required
def add(request):
    parameters = Parameter.objects.filter(status__gt=0).all()
    return render(request, 'parameter/add.html', {'parameters': parameters})


@login_required
def detail(request, sid):
    parameter = get_object_or_404(Parameter, pk=sid)
    return render(request, 'parameter/detail.html', {'parameter': parameter})


@login_required
def edit(request, sid):
    parameter = Parameter.objects.get(pk=sid)
    return render(request, 'parameter/edit.html', {'parameter': parameter})


@login_required
def parameter_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        parameter_list = Parameter.objects.filter(name__contains=key).order_by('-create_time').all()
    else:
        parameter_list = Parameter.objects.order_by('-create_time').all()
    paginator = Paginator(parameter_list, limit)
    try:
        parameters = paginator.page(page)
    except PageNotAnInteger:
        parameters = paginator.page(1)
    except EmptyPage:
        parameters = paginator.page(paginator.num_pages)
    for p in parameters:
        tmp = dict()
        tmp['id'] = p.id
        tmp['name'] = p.name
        tmp['code'] = p.code
        tmp['val'] = p.val
        tmp['type'] = p.type
        tmp['note'] = p.note
        tmp['create_time'] = str(p.create_time)
        tmp['update_time'] = str(p.update_time)
        if p.status == 1:
            status_str = '已开启'
        elif p.status == 0:
            status_str = '已关闭'
        else:
            status_str = '已删除'
        tmp['status'] = status_str
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(parameter_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = Parameter.objects.filter(pk__in=sids).all()
    for d_p in del_list:
        log = log_deletion(request, d_p, msg)
        try:
            Parameter.objects.filter(pk=d_p.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e.message)
            msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def insert(request):
    data = dict()
    status = False
    name = str(request.POST['name'])
    type = str(request.POST['type'])
    code = str(request.POST['code'])
    val = str(request.POST['val'])
    note = str(request.POST['note'])
    if Parameter.objects.filter(code=code):
        msg = '参数编码 %s 已存在' % code
    else:
        parameter = Parameter(name=name, code=code, type=type, val=val, note=note)
        try:
            parameter.save()
            status = True
            msg = '添加成功'
        except Exception as e:
            msg = e
        log_addition(request, parameter, msg)
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
    type = int(request.POST['type'])
    code = str(request.POST['code'])
    val = str(request.POST['val'])
    note = str(request.POST['note'])
    p = Parameter.objects.get(pk=sid)
    try:
        Parameter.objects.filter(pk=sid).update(name=name, type=type, code=code, val=val, note=note)
        msg = '修改成功'
        status = True
    except Exception as e:
        msg = e
    log_change(request, p, msg)
    data['msg'] = msg
    data['status'] = status
    return HttpResponse(json.dumps(data), content_type="application/json")
