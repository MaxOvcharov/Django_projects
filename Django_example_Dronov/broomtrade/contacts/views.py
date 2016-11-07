from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from generic.mixins import CategoryListMixin
from contacts.models import MailList

class ContactsView(SuccessMessageMixin, CreateView, CategoryListMixin):
  model = MailList
  template_name = "contacts.html"
  success_url = reverse_lazy("contacts")
  success_message = "Вы успешно добавлены в список рассылки"
