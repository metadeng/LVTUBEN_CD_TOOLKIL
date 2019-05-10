from django.urls import path

from parameter import views

app_name = 'parameter'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('insert/', views.insert, name='insert'),
    path('parameter_list/', views.parameter_list, name='parameter_list'),
    path('delete/', views.delete, name='delete'),
    path('detail/<int:sid>/', views.detail, name='detail'),
    path('edit/<int:sid>/', views.edit, name='edit'),
    path('update/', views.update, name='update'),

]
