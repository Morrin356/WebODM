from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from .views import app as app_views, public as public_views, dev as dev_views
from .plugins.views import app_view_handler, root_url_patterns

from app.boot import boot
from webodm import settings
from app.plugins import sync_plugin_db

# Test cases call boot() independently
# Also don't execute boot with celery workers
if not settings.WORKER_RUNNING and not settings.TESTING:
    boot()

# During testing, boot() is not called (see above)
# but we need to know which plugins are available to mount the proper
# routes via urlpatterns.
if settings.TESTING:
    sync_plugin_db()

urlpatterns = [
    path(r'^$', app_views.index, name='index'),
    path(r'^welcome/$', app_views.welcome, name='welcome'),
    path(r'^dashboard/$', app_views.dashboard, name='dashboard'),
    path(r'^map/project/(?P<project_pk>[^/.]+)/task/(?P<task_pk>[^/.]+)/$', app_views.map, name='map'),
    path(r'^map/project/(?P<project_pk>[^/.]+)/$', app_views.map, name='map'),
    path(r'^3d/project/(?P<project_pk>[^/.]+)/task/(?P<task_pk>[^/.]+)/$', app_views.model_display, name='model_display'),

    path(r'^public/task/(?P<task_pk>[^/.]+)/map/$', public_views.map, name='public_map'),
    path(r'^public/task/(?P<task_pk>[^/.]+)/iframe/map/$', public_views.map_iframe, name='public_iframe_map'),
    path(r'^public/task/(?P<task_pk>[^/.]+)/3d/$', public_views.model_display, name='public_3d'),
    path(r'^public/task/(?P<task_pk>[^/.]+)/iframe/3d/$', public_views.model_display_iframe, name='public_iframe_3d'),
    path(r'^public/task/(?P<task_pk>[^/.]+)/json/$', public_views.task_json, name='public_json'),

    path(r'^processingnode/([\d]+)/$', app_views.processing_node, name='processing_node'),

    path(r'^api/', include("app.api.urls")),

    path(r'^plugins/(?P<plugin_name>[^/.]+)/(.*)$', app_view_handler),

    path(r'^about/$', app_views.about, name='about'),
    path(r'^dev-tools/(?P<action>.*)$', dev_views.dev_tools, name='dev_tools'),

    # TODO: add caching: https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#note-on-performance
    path(r'^jsi18n/', JavaScriptCatalog.as_view(packages=['app']), name='javascript-catalog'),
    path(r'^i18n/', include('django.conf.urls.i18n')),
] + root_url_patterns()

handler404 = app_views.handler404
handler500 = app_views.handler500

