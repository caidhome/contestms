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
from userms.views import Stu_LoginView, Admin_LoginView, LogoutView, ListView, AddView, UploadAvatorView, \
    ResetpwdView, DelView, Admin_PersonView, Stu_Query_PersonView, Stu_PersonView, Stu_InfoView, Email_code_APIView, StuUpdateInfo

urlpatterns = [
    re_path('^login$', Stu_LoginView.as_view(), name='login'),
    re_path('^admin/login$', Admin_LoginView.as_view(), name='admin_login'),
    re_path('^logout$', LogoutView.as_view(), name='logout'),
    re_path('^resetpwd/(\d+)/$', ResetpwdView.as_view(), name='resetpwd'),
    re_path('^add/(\d+)/$', AddView.as_view(), name='add'),
    re_path('^del/(\d+)/$', DelView.as_view(), name='del'),
    re_path('^upload$', UploadAvatorView.as_view(), name='upload'),
    re_path('^list/(\d+)/$', ListView.as_view(), name='list'),
    re_path('^person$', Admin_PersonView.as_view(), name='person'),
    re_path('^stu_query_person$', Stu_Query_PersonView.as_view(), name='stu_person'),
    re_path('^student/(\d+)/$', Stu_PersonView.as_view(), name='student'),
    re_path('^stu_info$', Stu_InfoView.as_view(), name='stu_info'),
    re_path('^codeapi$', Email_code_APIView.as_view(), name='codeapi'),
    re_path('^stueditinfo$', StuUpdateInfo.as_view(), name='stueditinfo'),
]
