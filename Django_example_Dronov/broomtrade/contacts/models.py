from django.db import models

class MailList(models.Model):
  username = models.CharField(max_length = 50, verbose_name = "Имя")
  email = models.EmailField(unique = True, verbose_name = "E-mail")
  
  class Meta:
    verbose_name = "посетитель"
    verbose_name_plural = "список рассылки"
