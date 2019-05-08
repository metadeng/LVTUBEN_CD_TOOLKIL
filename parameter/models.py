# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from LVTUBEN.models import BaseModel


class Parameter(BaseModel):
    name = models.CharField('参数名称', max_length=100)
    code = models.CharField('参数编码', max_length=200)
    val = models.CharField('参数取值', null=False, blank=True, max_length=200)
    type = models.IntegerField('参数类型', default=0, null=False, blank=True)
    note = models.CharField('参数说明', max_length=100)

    class Meta:
        verbose_name = '参数'
        db_table = 'parameter'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
