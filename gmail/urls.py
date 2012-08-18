from django.conf.urls.defaults import patterns, url
from gmail import views


urlpatterns = patterns('gmail.views',
    url(r'^$', views.HomePageView.as_view(), name="homepage"),
    url(r'^/about/$', views.AboutView.as_view(), name="about"),
    url(r'^signup/$', views.AccountAdd.as_view(), name="signup"),

    url(r'^/account/$', views.AccountView.as_view(), name="account-detail"),
    url(r'^/account/add/$', views.AccountAdd.as_view(), name="account-add"),
    url(r'^/account/list/$', views.AccountList.as_view(), name="account-list"),
    url(r'^/account/change/$', views.AccountChange.as_view(), name="account-change"),

    # url(r'^/client/$', 'client_detail', name="client-detail"),
    # url(r'^/client/add/$', 'client_add', name="client-add"),
    # url(r'^/client/list/$', 'client_list', name="client-list"),
    # url(r'^/client/change/$', 'client_change', name="client-change"),

    # url(r'^/profile/$', 'profile_detail', name="profile-detail"),
    # url(r'^/profile/add/$', 'profile_add', name="profile-add"),
    # url(r'^/profile/list/$', 'profile_list', name="profile-list"),
    # url(r'^/profile/change/$', 'profile_change', name="profile-change"),

    # url(r'^/contact/$', 'contact_detail', name="contact-detail"),
    # url(r'^/contact/add/$', 'contact_add', name="contact-add"),
    # url(r'^/contact/list/$', 'contact_list', name="contact-list"),
    # url(r'^/contact/change/$', 'contact_change', name="contact-change"),

    # url(r'^/message/$', 'message_detail', name="message-detail"),
    # url(r'^/message/add/$', 'message_add', name="message-add"),
    # url(r'^/message/list/$', 'message_list', name="message-list"),
    # url(r'^/message/change/$', 'message_change', name="message-change"),

    # url(r'^/link/add/$', 'link_add', name="link-add"),
    # url(r'^/link/list/$', 'link_list', name="link-list"),
    # url(r'^/link/change/$', 'link_change', name="link-change"),
)
