# coding: utf-8
from __future__ import unicode_literals

import sys

from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from journal.views import log_addition, log_change, log_grant, log_deletion

import json

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse


def index(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        return render(request, 'manage/index.html', {'user': user})
    else:
        return HttpResponseRedirect(reverse('login'))


def login(request):
    return render(request, 'manage/login.html')


@login_required
def setting(request):
    return render(request, 'manage/settings.html')


@login_required
def welcome(request):
    return render(request, 'manage/welcome.html')


@login_required
def user(request):
    return render(request, 'user/index.html')


@login_required
def group(request):
    return render(request, 'group/index.html')


@login_required
def permission(request):
    return render(request, 'permission/index.html')


@login_required
def password(request):
    return render(request, 'user/update_password.html')


@login_required
def user_add(request):
    groups = Group.objects.all()
    return render(request, 'user/add.html', {'groups': groups})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'group/detail.html', {'group': group})


@login_required
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    all_permission = Permission.objects.all()
    group_permission = group.permissions.all()
    rest_permission = [p for p in all_permission if p not in group_permission]
    return render(request, 'group/edit.html',
                  {'group': group, 'rest_permission': rest_permission})


@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    groups = Group.objects.all()
    return render(request, 'user/edit.html', {"user": user, "groups": groups})


@login_required
def user_grant(request, pk):
    user = get_object_or_404(User, pk=pk)
    all_permission = Permission.objects.all()
    user_permission = user.user_permissions.all()
    group_permission = list()
    for g in user.groups.all():
        for p in g.permissions.all():
            group_permission.append(p)
    group_permission = list(set(group_permission))
    rest_permission = [p for p in all_permission if p not in user_permission and p not in group_permission]

    return render(request, 'user/grant.html', {"user": user, 'rest_permission': rest_permission})


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user/detail.html', {'user': user})


@login_required
def permission_detail(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    return render(request, 'permission/detail.html', {'permission': permission})


@login_required
def group_add(request):
    permission = Permission.objects.all()
    return render(request, 'group/add.html', {'permission': permission})


@login_required
def permission_add(request):
    content_type = ContentType.objects.all()
    return render(request, 'permission/add.html', {'content_type': content_type})


@login_required
def permission_edit(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    content_type = ContentType.objects.all()
    return render(request, 'permission/edit.html', {'permission': permission, 'content_type': content_type})


@login_required
def user_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        user_list = User.objects.filter(username__contains=key).order_by('-date_joined').all()
    else:
        user_list = User.objects.order_by('-date_joined').all()
    paginator = Paginator(user_list, limit)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    for u in users:
        tmp = dict()
        tmp['id'] = u.id
        tmp['username'] = u.username
        tmp['first_name'] = u.first_name
        tmp['last_name'] = u.last_name
        tmp['email'] = u.email
        tmp['is_staff'] = u.is_staff
        tmp['is_active'] = u.is_active
        tmp['is_superuser'] = u.is_superuser
        if u.groups.all().first():
            tmp['group'] = u.groups.all().first().name
        tmp['last_login'] = str(u.last_login)
        tmp['date_joined'] = str(u.date_joined)
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(user_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def group_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        group_list = Group.objects.filter(name__contains=key).order_by('name').all()
    else:
        group_list = Group.objects.order_by('name').all()
    paginator = Paginator(group_list, limit)
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    for g in groups:
        tmp = dict()
        tmp['id'] = g.id
        tmp['name'] = g.name
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(group_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def permission_list(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    key = request.GET.get('key')
    data = dict()
    data_list = list()
    if key:
        permission_list = Permission.objects.filter(name__contains=key).order_by('content_type_id').all()
    else:
        permission_list = Permission.objects.order_by('content_type_id').all()
    paginator = Paginator(permission_list, limit)
    try:
        permissions = paginator.page(page)
    except PageNotAnInteger:
        permissions = paginator.page(1)
    except EmptyPage:
        permissions = paginator.page(paginator.num_pages)
    for p in permissions:
        tmp = dict()
        tmp['id'] = p.id
        tmp['name'] = p.name
        tmp['model'] = p.content_type.model
        tmp['codename'] = p.codename
        data_list.append(tmp)
    data['code'] = 0
    data['msg'] = ''
    data['data'] = data_list
    data['count'] = len(permission_list)
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def check_in(request):
    data = dict()
    username = str(request.POST['username'])
    password = str(request.POST['password'])
    status = False
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if user.is_staff:
                auth.login(request, user)
                status = True
                msg = ' %s 登录成功，正在为你加载系统。' % username
            else:
                msg = '该用户无权限进入系统，请联系管理员。'
        else:
            msg = '用户 %s 还未激活，请联系管理员。' % username
    else:
        msg = '用户名或密码不正确，请重新输入。'
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def user_insert(request):
    status = False
    data = dict()
    username = str(request.POST['username'])
    password = str(request.POST['password'])
    email = str(request.POST['email'])
    first_name = str(request.POST['first_name'])
    last_name = str(request.POST['last_name'])
    group = int(request.POST['group'])
    is_superuser = True if str(request.POST['is_superuser']) == 'true' else False
    is_staff = True if str(request.POST['is_staff']) == 'true' else False
    user = User.objects.filter(username=username).first()
    if user:
        msg = '用户 %s 已存在' % username
    else:
        if password == None or password == '':
            password = 'Aa123456'
            group = Group.objects.get(pk=group) if group else None
        my_user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                           last_name=last_name, is_superuser=is_superuser,
                                           is_staff=is_staff)
        try:
            my_user.groups.add(group)
            my_user.save()
            status = True
            msg = '添加成功'
        except Exception as e:
            msg = e.message
        log_addition(request, my_user, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def user_grant_update(request):
    data = dict()
    status = False
    sid = int(request.POST['sid'])
    permissions = request.POST.getlist('permissions[]')
    user = get_object_or_404(User, pk=sid)
    if user:
        try:
            pre_permissions = list(Permission.objects.filter(id__in=permissions).all())
            user.user_permissions.clear()
            user.user_permissions.set(pre_permissions)
            status = True
            msg = '授权成功'
        except Exception as e:
            msg = e
    else:
        msg = '未获取到用户信息，请稍后再试'
    log_grant(request, user, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def user_update(request):
    status = False
    data = dict()
    sid = int(request.POST['sid'])
    username = str(request.POST['username'])
    email = str(request.POST['email'])
    first_name = str(request.POST['first_name'])
    last_name = str(request.POST['last_name'])
    group = int(request.POST['group'])
    is_superuser = True if str(request.POST['is_superuser']) == 'true' else False
    is_staff = True if str(request.POST['is_staff']) == 'true' else False
    user = User.objects.get(pk=sid)
    try:
        pre_group = Group.objects.get(pk=group)
        User.objects.filter(pk=sid).update(username=username, email=email, first_name=first_name, last_name=last_name,
                                           is_superuser=is_superuser, is_staff=is_staff)
        user.groups.clear()
        user.groups.add(pre_group)
        status = True
        msg = '修改成功'
    except Exception as e:
        msg = e
    log_change(request, user, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def user_delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = User.objects.filter(pk__in=sids).all()
    for d_u in del_list:
        log = log_deletion(request, d_u, msg)
        try:
            User.objects.filter(pk=d_u.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e.message)
            msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def group_insert(request):
    data = dict()
    status = False
    name = str(request.POST['name'])
    permissions = request.POST.getlist('permissions[]')
    group = Group.objects.filter(name=name).first()
    if group:
        msg = ' %s 用户组已存在' % name
    else:
        pre_permissions = Permission.objects.filter(id__in=permissions).all()
        g = Group(name=name)
        try:
            g.save()
            for p in pre_permissions:
                g.permissions.add(p)
            g.save()
            status = True
            msg = '添加成功'
        except Exception as e:
            msg = e
        log_addition(request, g, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def group_update(request):
    data = dict()
    status = False
    name = str(request.POST['name'])
    sid = int(request.POST['sid'])
    permissions = request.POST.getlist('permissions[]')
    group = Group.objects.get(pk=sid)
    if group:
        try:
            pre_permissions = Permission.objects.filter(id__in=permissions).all()
            group.name = name
            group.permissions.clear()
            for p in pre_permissions:
                group.permissions.add(p)
            group.save()
            status = True
            msg = '修改成功'
        except Exception as e:
            msg = e
        log_change(request, group, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def permission_insert(request):
    data = dict()
    status = False
    name = str(request.POST['name'])
    codename = str(request.POST['codename'])
    content_type = int(request.POST['content_type']) if request.POST['content_type'] else None
    permission = Permission.objects.filter(name=name).first()
    if permission:
        msg = ' %s 权限已存在' % name
    else:
        if content_type:
            ct = ContentType.objects.get(pk=content_type)
        else:
            ct = None
        p = Permission(name=name, codename=codename)
        p.content_type = ct
        try:
            p.save()
            status = True
            msg = '添加成功'
        except Exception as e:
            msg = e
        log_addition(request, p, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def permission_update(request):
    data = dict()
    status = False
    sid = int(request.POST['sid'])
    name = str(request.POST['name'])
    codename = str(request.POST['codename'])
    content_type = int(request.POST['content_type']) if request.POST['content_type'] else None
    p = Permission.objects.get(pk=sid)
    if content_type:
        try:
            ct = ContentType.objects.get(pk=content_type)
            Permission.objects.filter(pk=sid).update(name=name, codename=codename, content_type=ct)
            status = True
            msg = '修改成功'
        except Exception as e:
            msg = e
    else:
        msg = '未查询到应用，请稍后再试'
    log_change(request, p, msg)
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def group_delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = Group.objects.filter(pk__in=sids).all()
    for d_g in del_list:
        log = log_deletion(request, d_g, msg)
        try:
            Group.objects.filter(pk=d_g.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e.message)
            msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@csrf_exempt
def permission_delete(request):
    data = dict()
    sids = request.POST.getlist('sids[]')
    status = False
    msg = '删除成功'
    del_list = Permission.objects.filter(pk__in=sids).all()
    for d_p in del_list:
        log = log_deletion(request, d_p, msg)
        try:
            Permission.objects.filter(pk=d_p.id).delete()
            status = True
        except Exception as e:
            LogEntry.objects.filter(pk=log.pk).update(change_message=e.message)
            msg = e.message
    data['status'] = status
    data['msg'] = msg
    return HttpResponse(json.dumps(data), content_type="application/json")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))
