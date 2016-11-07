from django.contrib import admin
from imagepool.models import ImagePool

class ImagePoolAdmin(admin.ModelAdmin):
  list_display = ("user", "uploaded", "image")
  list_display_links = ("user", "uploaded")
  date_hierarchy = "uploaded"
  list_filter = ("user",)

admin.site.register(ImagePool, ImagePoolAdmin)
