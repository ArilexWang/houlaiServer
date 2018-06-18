"""houlai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from iosapp import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^loginWithoutCode/', views.loginWithoutCode),
    url(r'^loginWithCode/', views.loginWithCode),
    url(r'^loadAllComments/', views.loadAllComments),
    url(r'^loadCommentByDayid/', views.loadCommentByDayid),
    url(r'^createComment/', views.createComment),
]
