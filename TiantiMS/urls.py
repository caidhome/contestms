from django.views import static ##新增
from django.conf import settings ##新增
from django.conf.urls import url ##新增
from django.urls import path, include, re_path
from userms.views import Admin_IndexView, WelcomeView, Stu_IndexView, page_not_found, page_error

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^cert/', include(('certms.urls', 'certms'), namespace='certms')),
    re_path(r'^user/', include(('userms.urls', 'userms'), namespace='userms')),
    re_path(r'^contest/', include(('contestms.urls', 'contestms'), namespace='contestms')),
    re_path('^admin/index$', Admin_IndexView.as_view(), name='admin_index'),
    re_path('^$', Stu_IndexView.as_view(), name='index'),
    re_path('^welcome$', WelcomeView.as_view(), name='welcome'),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #     {'document_root': settings.STATIC_ROOT}, name='static'),
]


# handler404 = 'userms.views.page_not_found'
# handler500 = 'userms.views.page_error'