from django.conf.urls.defaults import *
from django.conf import settings
from blog import views

urlpatterns = patterns(
    '',
    url(r'^$', views.BlogIndex.as_view(), {}, name='index'),
    url(r'^new/$', views.new_post, {}, name='new-post'),
    url(r'^(?P<blog_name>.+)/(?P<post_key_name>[a-zA-Z0-9-_]+)/edit/$',
        views.edit_post, {}, name='edit-post'),
    url(r'^(?P<blog_name>.+)/(?P<post_key_name>[a-zA-Z0-9-_]+)/delete/$',
        views.delete_post, {}, name='delete-post'),
    url(r'^(?P<blog_name>.+)/(?P<post_key_name>[a-zA-Z0-9-_]+)/$', views.post_detail, {}, name='post_detail'),
    url(r'^__exception_test__/$', views.exception_test, {}),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
        )
