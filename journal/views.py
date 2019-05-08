# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_exempt

from utils.log_action_util import flag2action


@login_required
def index(request):
    return render(request, 'journal/index.html')


@login_required
def journal_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        journal_list = LogEntry.objects.filter(change_message__contains=key).order_by('-action_time').all()
    else:
        journal_list = LogEntry.objects.order_by('-action_time').all()
    paginator = Paginator(journal_list, limit)
    try:
        journals = paginator.page(page)
    except PageNotAnInteger:
        journals = paginator.page(1)
    except EmptyPage:
        journals = paginator.page(paginator.num_pages)
    for j in journals:
        tmp = dict()
        tmp['id'] = j.id
        tmp['action_time'] = str(j.action_time)
        tmp['user'] = j.user.username
        tmp['model'] = j.content_type.model
        tmp['object_id'] = j.object_id
        tmp['object_repr'] = str(j.object_repr)
        tmp['action_flag'] = flag2action(j.action_flag)
        tmp['msg'] = str(j.change_message)
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(journal_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    try:
        LogEntry.objects.filter(pk__in=sids).delete()
        msg = '删除成功'
        status = True
    except Exception as e:
        print(e.message)
        msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def detail(request, sid):
    log = get_object_or_404(LogEntry, pk=sid)
    return render(request, 'journal/detail.html', {'log': log})


def log_addition(request, object, message):
    from django.contrib.admin.models import LogEntry, ADDITION
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=ADDITION,
        change_message=message,
    )


def log_change(request, object, message):
    from django.contrib.admin.models import LogEntry, CHANGE
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=CHANGE,
        change_message=message,
    )


def log_grant(request, object, message):
    from django.contrib.admin.models import LogEntry
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=4,
        change_message=message,
    )


def log_deletion(request, object, message):
    from django.contrib.admin.models import LogEntry, DELETION
    return LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=DELETION,
        change_message=message,
    )
