from django.urls import path, re_path

from main import views

urlpatterns = [
    path('issue/', views.KeyIssue.as_view(), name='key_issue'),
    re_path(r'^check/(?P<key_value>([A-Za-z0-9]){4})/$', views.KeyCheck.as_view(), name='key_check'),
    re_path(r'^expire/(?P<key_value>([A-Za-z0-9]){4})/$', views.KeyExpire.as_view(), name='key_expire'),
    path('new_keys_counter/', views.NewKeysCounterView.as_view(), name='new_keys_counter'),
]
