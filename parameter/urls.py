from django.urls import path

from parameter import views

app_name = 'parameter'
urlpatterns = [
    path('', views.index, name='index'),
]
