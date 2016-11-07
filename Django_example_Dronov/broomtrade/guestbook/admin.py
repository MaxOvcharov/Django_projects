from django.contrib import admin
from guestbook.models import Guestbook

class GuestbookAdmin(admin.ModelAdmin):
  list_display = ("posted", "user", "content")
  search_fields = ("user", "content")
  date_hierarchy = 'posted'

admin.site.register(Guestbook, GuestbookAdmin)
