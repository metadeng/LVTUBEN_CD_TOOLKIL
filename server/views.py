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
from server.models import Server


@login_required
def index(request):
    return render(request, 'server/index.html')


@login_required
def add(request):
    server = Server.objects.filter(status__gt=0).all()
    return render(request, 'server/add.html', {'server': server})


@login_required
def detail(request, sid):
    server = get_object_or_404(Server, pk=sid)
    return render(request, 'server/detail.html', {'server': server})


@login_required
def edit(request, sid):
    server = Server.objects.get(pk=sid)
    return render(request, 'server/edit.html', {'server': server})


@login_required
def server_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        server_list = Server.objects.filter(ip__contains=key).order_by('-create_time').all()
    else:
        server_list = Server.objects.order_by('-create_time').all()
    paginator = Paginator(server_list, limit)
    try:
        servers = paginator.page(page)
    except PageNotAnInteger:
        servers = paginator.page(1)
    except EmptyPage:
        servers = paginator.page(paginator.num_pages)
    for s in servers:
        tmp = dict()
        tmp['id'] = s.id
        tmp['ip'] = s.ip
        tmp['os'] = s.os
        tmp['username'] = s.username
        tmp['password'] = s.password
        tmp['ssh_port'] = s.ssh_port
        tmp['create_time'] = str(s.create_time)
        tmp['update_time'] = str(s.update_time)
        if s.status == 1:
            status_str = '已开启'
        elif s.status == 0:
            status_str = '已关闭'
        else:
            status_str = '已删除'
        tmp['status'] = status_str
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(server_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = Server.objects.filter(pk__in=sids).all()
    for d_p in del_list:
        log = log_deletion(request, d_p, msg)
        try:
            Server.objects.filter(pk=d_p.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e)
            msg = e
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def insert(request):
    data = dict()
    status = False
    msg = '添加成功'
    try:
        ip = str(request.POST['ip'])
        os = str(request.POST['os'])
        ssh_port = int(request.POST['ssh_port'])
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        if Server.objects.filter(ip=ip):
            msg = '服务器 %s 已存在' % ip
        else:
            server = Server(ip=ip, os=os, ssh_port=ssh_port, username=username, password=password)
            server.save()
            status = True
            msg = '添加成功'
            log_addition(request, server, msg)
    except Exception as e:
        msg = '系统错误，添加失败'
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def update(request):
    data = dict()
    status = False
    sid = int(request.POST['sid'])
    ip = str(request.POST['ip'])
    os = str(request.POST['os'])
    ssh_port = int(request.POST['ssh_port'])
    username = str(request.POST['username'])
    password = str(request.POST['password'])
    p = Server.objects.get(pk=sid)
    try:
        Server.objects.filter(pk=sid).update(ip=ip, os=os, ssh_port=ssh_port, username=username, password=password)
        msg = '修改成功'
        status = True
    except Exception as e:
        msg = e
    log_change(request, p, msg)
    data['msg'] = msg
    data['status'] = status
    return HttpResponse(json.dumps(data), content_type="application/json")
