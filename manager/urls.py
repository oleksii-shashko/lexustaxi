from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='manager'),

    url(r'report/(?P<start>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})', views.report, name='report_view'),
    url(r'report_download/', views.report_download, name='report_download'),
]