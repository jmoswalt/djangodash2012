from django.conf.urls.defaults import patterns, url
from oldmail import views


urlpatterns = patterns('oldmail.views',
    url(r'^$', views.AccountView.as_view(), name="account_detail"),
    url(r'^change/$', views.AccountChangeView.as_view(), name="account_change"),

    url(r'^oauth2/$', 'authenticate', name="authenticate"),
    url(r'^oauth2callback/$', 'authenticate_callback', name="authenticate_callback"),

    # url(r'^client/$', 'client_detail', name="client_detail"),
    url(r'^client/add/$', views.ClientCreate.as_view(), name="client_add"),
    url(r'^client/list/$', views.ClientList.as_view(), name="client_list"),
    url(r'^client/change/(?P<pk>\d+)/$', views.ClientChange.as_view(), name="client_change"),

    # url(r'^profile/$', 'profile_detail', name="profile_detail"),
    # url(r'^profile/add/$', 'profile_add', name="profile_add"),
    url(r'^profile/list/$', views.ProfileList.as_view(), name="profile_list"),
    url(r'^profile/change/(?P<pk>\d+)/$', views.ProfileChange.as_view(), name="profile_change"),

    # url(r'contact/$', 'contact_detail', name="contact_detail"),
    url(r'^contact/add/$', views.ContactCreate.as_view(), name="contact_add"),
    url(r'^contact/list/$', views.ContactList.as_view(), name="contact_list"),
    url(r'^contact/change/(?P<pk>\d+)/$', views.ContactChange.as_view(), name="contact_change"),

    # url(r'^message/$', 'message_detail', name="message_detail"),
    # url(r'^message/add/$', 'message_add', name="message_add"),
    # url(r'^message/list/$', 'message_list', name="message_list"),
    # url(r'^message/change/$', 'message_change', name="message_change"),

    # url(r'^link/add/$', 'link_add', name="link_add"),
    # url(r'^link/list/$', 'link_list', name="link_list"),
    # url(r'^link/change/$', 'link_change', name="link_change"),
)
