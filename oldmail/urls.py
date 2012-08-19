from django.conf.urls.defaults import patterns, url
from oldmail import views


urlpatterns = patterns('oldmail.views',
    url(r'^$', views.AccountView.as_view(), name="account_detail"),
    url(r'^invite/$', views.AccountInviteView.as_view(), name="account_invite"),
    url(r'^change/$', views.AccountChangeView.as_view(), name="account_change"),

    url(r'^getmail/$', 'get_mail', name="get_mail"),

    url(r'^oauth1/$', 'oauth_connect', name="oauth_connect"),

    url(r'^oauth2/$', 'oauth2', name="oauth2"),
    url(r'^oauth2callback/$', 'oauth2_callback', name="oauth2_callback"),

    url(r'^oauth/$', 'get_request_token', name="get_request_token"),
    url(r'^oauthcallback/$', 'oauth_callback', name="oauth_callback"),

    url(r'^profile/activate/(?P<random_string>[\w]+)/$', views.ProfileAddView.as_view(), name="profile_activate"),
    url(r'^profile/verify/(?P<random_string>[\w]+)/$', views.ProfileVerifyView.as_view(), name="profile_verify"),
    url(r'^profile/list/$', views.ProfileList.as_view(), name="profile_list"),
    url(r'^profile/change/(?P<pk>\d+)/$', views.ProfileChange.as_view(), name="profile_change"),

    url(r'^client/(?P<pk>\d+)/$', views.ClientDetail.as_view(), name="client_detail"),
    url(r'^client/add/$', views.ClientCreate.as_view(), name="client_add"),
    url(r'^client/list/$', views.ClientList.as_view(), name="client_list"),
    url(r'^client/change/(?P<pk>\d+)/$', views.ClientChange.as_view(), name="client_change"),
    url(r'^client/(?P<pk>\d+)/messages/$', views.ClientMessageList.as_view(), name="client_message_list"),

    url(r'^contact/add/$', views.ContactCreate.as_view(), name="contact_add"),
    url(r'^contact/list/$', views.ContactList.as_view(), name="contact_list"),
    url(r'^contact/change/(?P<pk>\d+)/$', views.ContactChange.as_view(), name="contact_change"),
    url(r'^contact/(?P<pk>\d+)/$', views.ContactMessageList.as_view(), name="contact_message_list"),

    url(r'^message/(?P<pk>\d+)/$', views.MessageView.as_view(), name="message_detail"),

    url(r'^search/$', views.SearchView.as_view(), name="search"),
)
