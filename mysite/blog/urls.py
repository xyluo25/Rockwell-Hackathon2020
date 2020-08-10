# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 26th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from django.urls import path,include

from . import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('viewhtmlfile/', views.viewhtmlfile, name='viewhtmlfile'),
    path("viewlink_kepler/",views.viewlink_kepler,name="viewlink_kepler"),
    path("viewhtml_str/",views.viewhtml_str,name="viewhtml_str"),
    path("viewCSV_local/",views.viewCSV_local,name="viewCSV_local"),
    path("viewCSV_webupload/",views.viewCSV_webupload,name="viewCSV_webupload"),
    path("viewcharts/",views.viewcharts,name="viewcharts"),
    path("viewplotlyfigure/",views.viewplotlyfigure,name="viewplotlyfigure"),
    path("viewupload/",views.viewupload,name="viewupload")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)