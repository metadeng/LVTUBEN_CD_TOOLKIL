from django.urls import path

from toolbar import views

app_name = 'toolbar'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('insert/', views.insert, name='insert'),
    path('edit/<int:sid>/', views.edit, name='edit'),
    path('update/', views.update, name='update'),
    path('toolbar_list/', views.toolbar_list, name='toolbar_list'),
    path('delete/', views.delete, name='delete'),
    path('detail/<int:sid>/', views.detail, name='detail'),
]
