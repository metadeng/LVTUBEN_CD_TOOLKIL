# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from LVTUBEN.models import BaseModel


class Server(BaseModel):
    ip = models.CharField('IP地址', max_length=20)
    os = models.CharField('操作系统', max_length=40)
    username = models.CharField('服务器用户名', max_length=40)
    password = models.CharField('用户密码', max_length=40)
    ssh_port = models.IntegerField('ssh连接端口', default=22)

    class Meta:
        db_table = 'server'
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.ip
