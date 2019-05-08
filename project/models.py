# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from LVTUBEN.models import BaseModel


class Project(BaseModel):
    name = models.CharField('项目名称', max_length=200)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    charger = models.ForeignKey(User, verbose_name='负责人', related_name='projects', on_delete=models.DO_NOTHING)
    participator = models.ManyToManyField(User, verbose_name='参与者')
    version = models.CharField('版本号', max_length=100)
    gitlab = models.CharField('代码地址', max_length=200)
    tag = models.CharField('git标记', max_length=100)
    note = models.TextField('项目简介')

    class Meta:
        db_table = 'project'
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.name
