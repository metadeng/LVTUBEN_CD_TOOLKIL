# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from project.models import Project


@login_required
def index(request):
    return render(request, 'report/index.html')


@login_required
def add(request):
    projects = Project.objects.filter(status__gt=0).all()
    return render(request, 'report/add.html', {'projects': projects})
