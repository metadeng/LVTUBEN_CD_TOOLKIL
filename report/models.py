# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from LVTUBEN.models import BaseModel
from project.models import Project


class ReportItem(BaseModel):
    project = models.ForeignKey(Project, verbose_name='报告项目', related_name='ReportItem', on_delete=models.DO_NOTHING)
    content = models.TextField('报告内容')
    completion = models.FloatField('完成进度', default=0)

    class Meta:
        db_table = 'report_item'
        verbose_name = '报告项'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.name


class Report(BaseModel):
    title = models.CharField('报告标题', max_length=200)
    author = models.ForeignKey(User, verbose_name='报告人', related_name='reports', on_delete=models.DO_NOTHING)
    report_item = models.ManyToManyField(ReportItem, verbose_name='报告项')

    class Meta:
        db_table = 'report'
        verbose_name = '报告'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.title
