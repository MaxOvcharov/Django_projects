from django.db import models
from datetime import datetime
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.comments.moderation import CommentModerator, moderator

class Blog(models.Model):
  title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
  description = models.TextField(verbose_name = "Краткое содержание")
  content = models.TextField(verbose_name = "Полное содержание")
  posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
  is_commentable = models.BooleanField(default = True, verbose_name = "Разрешены комментарии")
  tags = TaggableManager(blank = True, verbose_name = "Теги")
  user = models.ForeignKey(User, editable = False)

  def get_absolute_url(self):
    return reverse("blog_detail", kwargs = {"pk": self.pk})
  
  class Meta:
    ordering = ["-posted"]
    verbose_name = "статья блога"
    verbose_name_plural = "статьи блога"

class BlogModerator(CommentModerator):
  email_notification = True
  enable_field = "is_commentable"

moderator.register(Blog, BlogModerator)
