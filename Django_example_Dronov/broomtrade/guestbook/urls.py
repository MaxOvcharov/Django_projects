from django.conf.urls import patterns, url

from guestbook.views import GuestbookView

urlpatterns = patterns('',
  url(r'^$', GuestbookView.as_view(), name = "guestbook"),
)
