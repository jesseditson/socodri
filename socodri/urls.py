from django.conf.urls import include, patterns, url
from socodri import views


urlpatterns = patterns('',
    (r'^ping/$', views.ping),
    (r'^$', views.show_app),
)
