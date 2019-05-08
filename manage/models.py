# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from LVTUBEN.models import BaseModel


class UserInfo(BaseModel):
    user = models.OneToOneField(User, verbose_name='用户', on_delete=models.DO_NOTHING)
    avatar = models.ImageField('用户头像', upload_to='attachment/avatar/%Y/%m/%d/',
                               max_length=200, blank=True, null=True)
    role_id = models.IntegerField('用户角色', default=1)
    mobile = models.CharField('手机号码', max_length=100, null=True, blank=True)
    phone = models.CharField('座机号码', max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username
