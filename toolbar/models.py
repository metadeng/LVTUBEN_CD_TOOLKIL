# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from LVTUBEN.models import BaseModel
from plate.models import Plate


class Toolbar(BaseModel):
    name = models.CharField('工具名称', max_length=40)
    alias = models.CharField('英文名称', max_length=100)
    title = models.CharField('工具标题', max_length=100)
    icon = models.CharField('工具图标', max_length=200)
    avatar = models.ImageField('工具图片', upload_to='attachment/toolbar/%Y/%m/%d/', max_length=200, blank=True, null=True)
    note = models.TextField('工具简介')
    hits = models.IntegerField('点击量', default=1)
    stick = models.BooleanField('置顶', default=False)
    https = models.BooleanField('https请求', default=False)
    server = models.CharField('服务器', max_length=20)
    port = models.BigIntegerField('运行端口', default=80)
    color = models.CharField('展示颜色', default='#000000', max_length=20)
    plate = models.ForeignKey(Plate, verbose_name='所属导航', related_name='toolbar', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'toolbar'
        verbose_name = '工具'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.name
