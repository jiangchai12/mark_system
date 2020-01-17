"""markingsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from marking import views


urlpatterns = [
    re_path('^admin/', admin.site.urls),
    # re_path('^$', views.index, name="index"),
    re_path('^$', views.mark, name="mark"),
    re_path('^history_mark/', views.history_mark, name="history_mark"),
    # re_path('^host/multi_cmd/', views.multi_cmd, name="multi_cmd"),
    # re_path('^host/multi_file_transfer', views.multi_file_transfer, name="multi_file_transfer"),
    re_path('^mark/', views.mark, name="mark"),
    re_path('^account/login/', views.acc_login, name="acc_login"),
]
