from django.urls import path

from server import views

app_name = 'server'
urlpatterns = [
    path('', views.index, name='index'),
path('add/', views.add, name='add'),
    path('insert/', views.insert, name='insert'),
    path('server_list/', views.server_list, name='server_list'),
    path('delete/', views.delete, name='delete'),
    path('detail/<int:sid>/', views.detail, name='detail'),
    path('edit/<int:sid>/', views.edit, name='edit'),
    path('update/', views.update, name='update'),
]
