# coding:utf-8
from django.urls import path
from plate import views

app_name = 'plate'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/<int:sid>/', views.edit, name='edit'),
    path('insert/', views.insert, name='insert'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('detail/<int:sid>/', views.detail, name='detail'),
    path('plate_list/', views.plate_list, name='plate_list'),
]
