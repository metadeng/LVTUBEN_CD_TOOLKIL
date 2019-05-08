from django.urls import path

from sheet import views

app_name = 'sheet'
urlpatterns = [
    path('', views.index, name='index'),
]
