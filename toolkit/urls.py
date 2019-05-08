# coding=utf-8
from django.urls import path
from toolkit import views

app_name = 'toolkit'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/<int:sid>', views.list, name='list'),

]
