from django.conf.urls import patterns, url, include
from django.views.generic.simple import redirect_to
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from oldmail import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oldmail.views.home', name='home'),
    # url(r'^oldmail/', include('oldmail.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomePageView.as_view(), name="homepage"),
    url(r'^about/$', views.AboutView.as_view(), name="about"),
    url(r'^signup/$', views.AccountAdd.as_view(), name="signup"),
    url(r'^accounts/list/$', views.AccountListView.as_view(), name="account_list"),

    url(r'^accounts/profile/$', redirect_to, {'url': '/'}),
    url(r'^accounts/login/$', redirect_to, {'url': '/auth/login/'}),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.STATIC_ROOT, }),
    url(r'^(?P<slug>[\w\-]+)/', include('oldmail.urls')),
)
