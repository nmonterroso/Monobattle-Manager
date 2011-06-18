from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('viewers.views',
    url(r'^$', 'index'),
    url(r'^manage', 'manage')
)