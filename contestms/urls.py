"""TiantiMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from contestms.views import ListView, AddView, DelView, DetialView, HeadView, SignView, \
    UploadScoreView,Sign_List_View, Sign_Check_View, Sign_GenCert_View, Sign_Person_View,\
    Sign_Score_View, Cert_download_View, Template_download_View, Downzip_Certs_View,\
    SendNoticeView

urlpatterns = [
    re_path('^list$', ListView.as_view(), name='list'),
    re_path('^add$', AddView.as_view(), name='add'),
    re_path('^delete$', DelView.as_view(), name='delete'),
    re_path('^detial/(\d+)/$', DetialView.as_view(), name='detial'),
    re_path('^sign/(\d+)/$', SignView.as_view(), name='sign'),
    re_path('^head/$', HeadView.as_view(), name='head'),
    re_path('^upload_score$', UploadScoreView.as_view(), name='upload_score'),
    re_path('^down_temp$', Template_download_View.as_view(), name='down_temp'),
    re_path('^sign/list/(\d+)/$', Sign_List_View.as_view(), name='sign_list'),
    re_path('^sign/person$', Sign_Person_View.as_view(), name='sign_person'),
    re_path('^sign/score/(\d+)/$', Sign_Score_View.as_view(), name='sign_score'),
    re_path('^sign/check/(\d+)/$', Sign_Check_View.as_view(), name='sign_check'),
    re_path('^sign/gen_cert/(\d+)/(\d+)/$', Sign_GenCert_View.as_view(), name='sign_gen_cert'),
    re_path('^sign/download/(\d+)/$', Cert_download_View.as_view(), name='dowload_cert'),
    re_path('^sign/down_cert_zip/(\d+)/$', Downzip_Certs_View.as_view(), name='down_cert_zip'),
    re_path('^sendnotice/(\d+)/$', SendNoticeView.as_view(), name='sendnotice'),
]
