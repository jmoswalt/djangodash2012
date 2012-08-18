from django.conf.urls.defaults import patterns, url

from oldmail import views


urlpatterns = patterns('oldmail.views',
    url(r'^account/$', views.AccountView.as_view(), name="account_detail"),
    #url(r'^/account/add/$', views.AccountAdd.as_view(), name="account_add"),
    url(r'^account/list/$', views.AccountListView.as_view(), name="account_list"),
    url(r'^account/change/$', views.AccountChangeView.as_view(), name="account_change"),

    url(r'^oauth2/$', 'authenticate', name="authenticate"),
    url(r'^oauth2callback/$', 'authenticate_callback', name="authenticate_callback"),

    # url(r'^client/$', 'client_detail', name="client_detail"),
    # url(r'^client/add/$', views.ClientCreate.as_view(), name="client_add"),
    # url(r'^client/list/$', 'client_list', name="client_list"),
    # url(r'^client/change/$', 'client_change', name="client_change"),

    # url(r'^profile/$', 'profile_detail', name="profile_detail"),
    # url(r'^profile/add/$', 'profile_add', name="profile_add"),
    # url(r'^profile/list/$', 'profile_list', name="profile_list"),
    # url(r'^profile/change/$', 'profile_change', name="profile_change"),

    # url(r'^contact/$', 'contact_detail', name="contact_detail"),
    # url(r'^contact/add/$', 'contact_add', name="contact_add"),
    # url(r'^contact/list/$', 'contact_list', name="contact_list"),
    # url(r'^contact/change/$', 'contact_change', name="contact_change"),

    # url(r'^message/$', 'message_detail', name="message_detail"),
    # url(r'^message/add/$', 'message_add', name="message_add"),
    # url(r'^message/list/$', 'message_list', name="message_list"),
    # url(r'^message/change/$', 'message_change', name="message_change"),

    # url(r'^link/add/$', 'link_add', name="link_add"),
    # url(r'^link/list/$', 'link_list', name="link_list"),
    # url(r'^link/change/$', 'link_change', name="link_change"),
)
