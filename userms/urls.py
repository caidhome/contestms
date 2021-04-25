from django.contrib import admin
from django.urls import path, include, re_path
from userms.views import Stu_LoginView, Admin_LoginView, LogoutView, ListView, AddView, UploadAvatorView, \
    ResetpwdView, DelView, Admin_PersonView, Stu_Query_PersonView, Stu_PersonView, Stu_InfoView, \
    Email_code_APIView, StuUpdateInfo, RegisterView, UploadStuView, CheckStunoView

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
    re_path('^register$', RegisterView.as_view(), name='stueditinfo'),
    re_path('^uploadstuinfo$', UploadStuView.as_view(), name='uploadstuinfo'),
    re_path('^checkstuno/$', CheckStunoView.as_view(), name='checkstuno'),
]
