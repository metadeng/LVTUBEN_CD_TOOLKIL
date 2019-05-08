"""LVTUBEN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path

from LVTUBEN import settings
from LVTUBEN.views import page_not_found
from toolkit.views import index

from manage.views import login, logout
from django.views.static import serve

handler404 = page_not_found

urlpatterns = [
    path('', index, name='navigate'),
    path('toolkit/', include('toolkit.urls')),
    path('manage/', include('manage.urls')),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('upload/<str:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
