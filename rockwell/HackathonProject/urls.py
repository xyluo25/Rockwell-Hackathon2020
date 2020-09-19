# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, August 30th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from django.urls import path,include

from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("viewAnimation/",views.viewAnimation,name="viewAnimation"),
    path("viewComputation/",views.viewComputation,name="viewComputation"),
    path("viesHomepage/",views.viewHomepage,name="viewHomepage"),
    path("viewAbout/",views.viewAbout,name="viewAbout")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)