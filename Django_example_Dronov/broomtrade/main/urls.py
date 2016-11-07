from django.conf.urls import patterns, url

from main.views import MainPageView

urlpatterns = patterns('',
  url(r'^$', MainPageView.as_view(), name = "main"),
)
