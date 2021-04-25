from django.contrib import admin
from django.urls import path, include, re_path
from certms.views import AddView, ListView, DelView

urlpatterns = [
    re_path('^add$', AddView.as_view(), name='add'),
    re_path('^list$', ListView.as_view(), name='list'),
    re_path('^del$', DelView.as_view(), name='del'),
]
