# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from journal.views import log_addition, log_deletion

import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from project.models import Project


@login_required
def index(request):
    return render(request, 'project/index.html')


@login_required
def add(request):
    chargers = User.objects.filter(is_active=True).all()
    participator = User.objects.filter(is_active=True).all()
    return render(request, 'project/add.html', {'chargers': chargers, 'participator': participator})


@login_required
def detail(request, sid):
    project = get_object_or_404(Project, pk=sid)
    return render(request, 'project/detail.html', {'project': project})


@login_required
@csrf_exempt
def insert(request):
    data = dict()
    status = False
    name = str(request.POST['name'])
    start_time = str(request.POST['start_time']) if request.POST['start_time'] else None
    end_time = str(request.POST['end_time']) if request.POST['end_time'] else None
    version = str(request.POST['version'])
    gitlab = str(request.POST['gitlab'])
    tag = str(request.POST['tag'])
    note = str(request.POST['note'])
    charger = int(request.POST['charger']) if request.POST['charger'] else None
    participators = request.POST.getlist('participator[]')
    if Project.objects.filter(name=name):
        msg = '项目 %s 已存在' % name
    else:
        project = Project(name=name, start_time=start_time, end_time=end_time, version=version, gitlab=gitlab,
                          tag=tag, note=note)
        if charger and User.objects.get(pk=charger):
            project.charger_id = charger
            try:
                project.save()
                if participators:
                    pre_participators = User.objects.filter(id__in=participators).all()
                    for p in pre_participators:
                        project.participator.add(p)
                    project.save()
                status = True
                msg = '添加成功'
            except Exception as e:
                msg = e
            log_addition(request, project, msg)
        else:
            msg = '未查询到负责人信息'
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def project_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        project_list = Project.objects.filter(name__contains=key).order_by('-create_time').all()
    else:
        project_list = Project.objects.order_by('-create_time').all()
    paginator = Paginator(project_list, limit)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    for p in projects:
        tmp = dict()
        tmp['id'] = p.id
        tmp['name'] = p.name
        tmp['start_time'] = str(p.start_time)
        tmp['end_time'] = str(p.end_time)
        tmp['charger'] = p.charger.username
        # tmp['participator'] = p.participator
        tmp['version'] = p.version
        tmp['gitlab'] = p.gitlab
        tmp['tag'] = p.tag
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
    data['count'] = len(project_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = Project.objects.filter(pk__in=sids).all()
    for d_p in del_list:
        log = log_deletion(request, d_p, msg)
        try:
            Project.objects.filter(pk=d_p.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e.message)
            msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")
