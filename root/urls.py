from django.contrib import admin
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('portal.config.urls')),
)

handler404 = 'portal.views.handle_404'

handler500 = 'portal.views.handle_500'

handler403 = 'portal.views.handle_403'
