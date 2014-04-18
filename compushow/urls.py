from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover ()

urlpatterns = patterns('',
    url(r'^$'          , 'votaciones.views.home'),
    url(r'^informacion$'      , 'votaciones.views.info'),
    url(r'^votaciones$', 'votaciones.views.votaciones'),
    url(r'^nominar_do$'            , 'votaciones.views.nominar_do'),
    url(r'^borrar_voto_nominacion$', 'votaciones.views.borrar_voto_nominacion'),
    url(r'^consultar_nombre$'      , 'votaciones.views.consultar_nombre'),
    url(r'^votar_do$', 'votaciones.views.votar_do'),
    url(r'^quitar_voto_do$', 'votaciones.views.quitar_voto_do'),
    url(r'^login$'     , 'votaciones.views.pagina_login'),
    url(r'^login_do$'  , 'votaciones.views.login_do'),
    url(r'^logout_do$' , 'votaciones.views.logout_do'),
    url(r'^signup_do$' , 'votaciones.views.signup_do'),
    #url(r'^filtrar$', 'votaciones.views.filtrar'),    
    #url(r'^funcion$'    , 'votaciones.views.funcion'),
    #url(r'^funcion_do$' , 'votaciones.views.funcion_do'),
    url(r'^limpiar_media', 'votaciones.views.limpiar_media'),

    #url del admin
    url(r'^admin/$', 'votaciones.views.adminAdmin'),
    url(r'^adminJocoza/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),

    url(r'^templates/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.TEMPLATE_DIRS[0],
    }),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.TEMPLATE_DIRS[0],
    }),
)