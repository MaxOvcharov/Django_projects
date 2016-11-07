from django.contrib import admin
from contacts.models import MailList

class MailListAdmin(admin.ModelAdmin):
  list_display = ("email", "username")
  search_fields = ("email", "username")
  ordering = ("email",)

admin.site.register(MailList, MailListAdmin)
