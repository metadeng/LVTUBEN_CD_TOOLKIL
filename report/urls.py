from django.urls import path

from report import views

app_name = 'report'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
]
