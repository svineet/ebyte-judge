from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'(?P<question_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'(?P<question_id>[0-9]+)/submit$', views.submit, name="submit"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^leaderboard/$', views.leaderboard, name="leaderboard"),
    url(r'^submissions/$', views.list_submissions, name="list_submissions")
]
