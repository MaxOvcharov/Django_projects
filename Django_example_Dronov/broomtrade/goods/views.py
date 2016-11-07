from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.exceptions import ObjectDoesNotExist
# import logging

from categories.models import Category
from goods.models import Good, GoodImage
from goods.forms import GoodForm
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView

# logger = logging.getLogger(__name__)

GoodImagesFormset = inlineformset_factory(Good, GoodImage, can_order = True)

class SortMixin(ContextMixin):
  sort = "0"
  order = "A"

  def get_context_data(self, **kwargs):
    context = super(SortMixin, self).get_context_data(**kwargs)
    context["sort"] = self.sort
    context["order"] = self.order
    return context

class GoodsListView(PageNumberView, ListView, SortMixin, CategoryListMixin):
  model = Good
  template_name = "goods_index.html"
  paginate_by = 2
  cat = None

  def get(self, request, *args, **kwargs):
    if self.kwargs["pk"] == None:
      self.cat = Category.objects.first()
    else:
      self.cat = Category.objects.get(pk = self.kwargs["pk"])
    # logger.debug(self.cat.name)
    return super(GoodsListView, self).get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(GoodsListView, self).get_context_data(**kwargs)
    context["category"] = self.cat
    return context

  def get_queryset(self):
    goods = Good.objects.filter(category = self.cat)
    if self.sort == "2":
      if self.order == "D":
        goods = goods.order_by("-in_stock", "name")
      else:
        goods = goods.order_by("in_stock", "name")
    elif self.sort == "1":
      if self.order == "D":
        goods = goods.order_by("-price", "name")
      else:
        goods = goods.order_by("price", "name")
    else:
      if self.order == "D":
        goods = goods.order_by("-name")
      else:
        goods = goods.order_by("name")
    return goods

class GoodDetailView(PageNumberView, DetailView, SortMixin, PageNumberMixin):
  model = Good
  template_name = "good.html"

class GoodCreate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
  template_name = "good_add.html"
  cat = None
  form = None
  formset = None

  def get(self, request, *args, **kwargs):
    if self.kwargs["pk"] == None:
      self.cat = Category.objects.first()
    else:
      self.cat = Category.objects.get(pk = self.kwargs["pk"])
    self.form = GoodForm(initial = {"category": self.cat})
    self.formset = GoodImagesFormset()
    return super(GoodCreate, self).get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(GoodCreate, self).get_context_data(**kwargs)
    context["category"] = self.cat
    context["form"] = self.form
    context["formset"] = self.formset
    return context

  def post(self, request, *args, **kwargs):
    self.form = GoodForm(request.POST, request.FILES)
    if self.form.is_valid():
      new_good = self.form.save()
      self.formset = GoodImagesFormset(request.POST, request.FILES, instance = new_good)
      if self.formset.is_valid():
        self.formset.save()
        messages.add_message(request, messages.SUCCESS, "Товар успешно добавлен")
        return redirect(reverse("goods_index", kwargs = {"pk": new_good.category.pk}) + "?page=" + self.request.GET["page"] + "&sort=" + self.request.GET["sort"] + "&order=" + self.request.GET["order"])
    if self.kwargs["pk"] == None:
      self.cat = Category.objects.first()
    else:
      self.cat = Category.objects.get(pk = self.kwargs["pk"])
    self.formset = GoodImagesFormset(request.POST, request.FILES)
    return super(GoodCreate, self).get(request, *args, **kwargs)

class GoodUpdate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
  good = None
  template_name = "good_edit.html"
  form = None
  formset = None

  def get(self, request, *args, **kwargs):
    self.good = Good.objects.get(pk = self.kwargs["pk"])
    self.form = GoodForm(instance = self.good)
    self.formset = GoodImagesFormset(instance = self.good)
    return super(GoodUpdate, self).get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(GoodUpdate, self).get_context_data(**kwargs)
    context["good"] = self.good
    context["form"] = self.form
    context["formset"] = self.formset
    return context

  def post(self, request, *args, **kwargs):
    self.good = Good.objects.get(pk = self.kwargs["pk"])
    self.form = GoodForm(request.POST, request.FILES, instance = self.good)
    self.formset = GoodImagesFormset(request.POST, request.FILES, instance = self.good)
    if self.form.is_valid():
      self.form.save()
      if self.formset.is_valid():
        self.formset.save()
        messages.add_message(request, messages.SUCCESS, "Товар успешно изменен")
        return redirect(reverse("goods_index", kwargs = {"pk": self.good.category.pk}) + "?page=" + self.request.GET["page"] + "&sort=" + self.request.GET["sort"] + "&order=" + self.request.GET["order"])
    return super(GoodUpdate, self).get(request, *args, **kwargs)

class GoodDelete(PageNumberView, DeleteView, SortMixin, PageNumberMixin):
  model = Good
  template_name = "good_delete.html"
  def post(self, request, *args, **kwargs):
    self.success_url = reverse("goods_index", kwargs = {"pk": Good.objects.get(pk = kwargs["pk"]).category.pk}) + "?page=" + self.request.GET["page"] + "&sort=" + self.request.GET["sort"] + "&order=" + self.request.GET["order"]
    messages.add_message(request, messages.SUCCESS, "Товар успешно удален")
    return super(GoodDelete, self).post(request, *args, **kwargs)

class RssGoodsListFeed(Feed):
  def get_object (self, request, *args, **kwargs):
    try:
      return Category.objects.get(pk = kwargs["pk"])
    except Category.DoesNotExist:
      raise ObjectDoesNotExist("Нет такой категории!")
  def title(self, obj):
    return "Товары, относящиеся к категории '" + obj.name + "' :: Веник-Торг"
  def description(self, obj):
    return self.title(obj)
  def link(self, obj):
    return reverse("goods_index", kwargs = {"pk": obj.pk})
  def categories(self, obj):
    return [obj.name]
  def items(self, obj):
    return Good.objects.filter(category = obj).order_by("name")
  def item_title(self, item):
    return item.name
  def item_description(self, item):
    return item.description
  def item_categories(self, item):
    return [item.category.name]
  def item_link(self, item):
    return reverse("goods_detail", kwargs = {"pk": item.pk})

class AtomGoodsListFeed(RssGoodsListFeed):
  feed_type = Atom1Feed
  subtitle = RssGoodsListFeed.description
