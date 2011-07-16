from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('viewers.views',
    url(r'^$', 'index'),
    url(r'^manage-action', 'manage_action'),
    url(r'^manage', 'manage'),
    url(r'^verify', 'verify'),
    url(r'^submit', 'submit')
)