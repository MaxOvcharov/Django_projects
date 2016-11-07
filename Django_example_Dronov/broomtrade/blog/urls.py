from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from blog.views import BlogListView, BlogDetailView, BlogCreate, BlogUpdate, BlogDelete

urlpatterns = patterns('',
  url(r'^$', BlogListView.as_view(), name = "blog_index"),
  url(r'^(?P<pk>\d+)/detail/$', BlogDetailView.as_view(), name = "blog_detail"),
  url(r'^add/$', permission_required("blog.add_blog")(BlogCreate.as_view()), name = "blog_add"),
  url(r'^(?P<pk>\d+)/edit/$', permission_required("blog.change_blog")(BlogUpdate.as_view()), name = "blog_edit"),
  url(r'^(?P<pk>\d+)/delete/$', permission_required("blog.delete_blog")(BlogDelete.as_view()), name = "blog_delete"),
)
