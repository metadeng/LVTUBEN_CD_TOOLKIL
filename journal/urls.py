from django.urls import path

from journal import views

app_name = 'journal'
urlpatterns = [
    path('', views.index, name='index'),
    path('journal_list/', views.journal_list, name='journal_list'),
    path('delete/', views.delete, name='delete'),
    path('detail/<int:sid>/', views.detail, name='detail'),
]
