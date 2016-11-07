#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
#from page import views
from page.twviews import GoodListView, GoodDetailView

'''
urlpatterns = (
	url(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name = 'index'),
	url(r'^good/(?P<good_id>\d+)/$', views.good, name = 'good'),
	)
'''

urlpatterns = (url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name = 'index'),
			   url(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name = 'good'))