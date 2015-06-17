from django.conf.urls import patterns, include, url

from bowling import views

urlpatterns = patterns('',
  url(r'^$', views.index),
  url(r'^scorecard/$', views.game_flow),
  url(r'^reset/$', views.washout),
)
