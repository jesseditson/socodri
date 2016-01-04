from django.conf.urls import include, patterns
from socodri import views, resources


urlpatterns = patterns('',
    (r'api/funnel/', include(resources.FunnelResource.urls())),
    (r'api/action/', include(resources.ActionResource.urls())),
    (r'api/stage/', include(resources.StageResource.urls())),
    (r'^ping/$', views.ping),
    (r'^.*/$', views.show_app),
    (r'^$', views.show_app)
)
