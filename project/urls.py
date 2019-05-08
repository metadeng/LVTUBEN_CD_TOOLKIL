from django.urls import path

from project import views

app_name = 'project'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('project_list/', views.project_list, name='project_list'),
    path('insert/', views.insert, name='insert'),
    path('detail/<int:sid>/', views.detail, name='detail'),
    path('delete/', views.delete, name='delete'),
]
