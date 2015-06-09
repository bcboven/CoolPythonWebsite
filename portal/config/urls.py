from portal import views
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    #User Authentication based views
    (r'^/?$', views.mainview),

    #General User Pages
    (r'^dashboard/?$', views.dashboard),

    #Home Page
    (r'^home/?$', views.home),

    #Wireless Page
    (r'^APconfig/?$', views.APconfig),

    #Certificate Configuration Page
    (r'^tunnel/?$', views.tunnel),

    #Connections Pages
    (r'^connections/?$', views.connections),\

    #Connections Pages
    (r'^advance/?$', views.advance),

    #view logs
    (r'^log/?$', views.getlog),

    #enable saife connect
    (r'^enable/?$', views.enable),

    #enable saife connect
    (r'^disable/?$', views.disable),

    #enable passthrough
    (r'^passthrough/?$', views.passthrough),




)

# lets us serve our media
if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)