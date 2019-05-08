# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from LVTUBEN.models import BaseModel


# Create your models here.

class Plate(BaseModel):
    name = models.CharField('导航名称', max_length=20)
    prefix = models.CharField('英文名称', max_length=40)
    summary = models.CharField('导航摘要', max_length=100)
    icon = models.CharField('导航图标', max_length=200)
    note = models.TextField('导航简介')
    hits = models.IntegerField('点击量', default=0)
    stick = models.BooleanField('置顶', default=False)

    class Meta:
        db_table = 'plate'
        verbose_name = '导航'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.name
