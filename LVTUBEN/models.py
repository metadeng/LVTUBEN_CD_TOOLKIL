# coding:utf-8
from __future__ import unicode_literals


from django.db import models


# Create your models here.
from django.utils import timezone


class BaseModel(models.Model):
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    status = models.IntegerField('状态', default=1)

    class Meta:
        abstract = True
