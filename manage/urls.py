# coding=utf-8
from django.urls import include, path

from manage import views

app_name = 'manage'
urlpatterns = [
    path('', views.index, name='index'),
    path('plate/', include('plate.urls'), name='plate'),
    path('parameter/', include('parameter.urls'), name='parameter'),
    path('journal/', include('journal.urls'), name='journal'),
    path('report/', include('report.urls'), name='report'),
    path('toolbar/', include('toolbar.urls'), name='toolbar'),
    path('server/', include('server.urls'), name='server'),
    path('sheet/', include('sheet.urls'), name='sheet'),
    path('project/', include('project.urls'), name='project'),

    path('welcome/', views.welcome, name='welcome'),
    path('setting/', views.setting, name='setting'),

    path('user/', views.user, name='user'),
    path('user_add/', views.user_add, name='user_add'),
    path('user_update/', views.user_update, name='user_update'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_insert/', views.user_insert, name='user_insert'),
    path('user_grant_update/', views.user_grant_update, name='user_grant_update'),
    path('user_delete/', views.user_delete, name='user_delete'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_grant/<int:pk>/', views.user_grant, name='user_grant'),
    path('user_detail/<int:pk>/', views.user_detail, name='user_detail'),

    path('group/', views.group, name='group'),
    path('group_add/', views.group_add, name='group_add'),
    path('group_update/', views.group_update, name='group_update'),
    path('group_list/', views.group_list, name='group_list'),
    path('group_insert/', views.group_insert, name='group_insert'),
    path('group_delete/', views.group_delete, name='group_delete'),
    path('group_detail/<int:pk>/', views.group_detail, name='group_detail'),
    path('group_edit/<int:pk>/', views.group_edit, name='group_edit'),

    path('permission/', views.permission, name='permission'),
    path('permission_add/', views.permission_add, name='permission_add'),
    path('permission_list/', views.permission_list, name='permission_list'),
    path('permission_update/', views.permission_update, name='permission_update'),
    path('permission_insert/', views.permission_insert, name='permission_insert'),
    path('permission_delete/', views.permission_delete, name='permission_delete'),
    path('permission_detail/<int:pk>/', views.permission_detail, name='permission_detail'),
    path('permission_edit/<int:pk>/', views.permission_edit, name='permission_edit'),

    path('password/', views.password, name='password'),
    path('check_in/', views.check_in, name='check_in'),

]
