# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, Http404
from page.models import Category, Good
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage

def index(request, cat_id):
	# Get page from the list
	try:
		page_num = request.GET['page']
	except KeyError:
		page_num = 1

	cats = Category.objects.all().order_by("name")
	if cat_id == None:
		cat = Category.objects.first()
	else:
		try:
			cat = Category.objects.get(pk = cat_id)
		except Category.DoesNotExist:
			raise Http404
	# Every pages consist of 10 goods
	paginator = Paginator(Good.objects.filter(category = cat).order_by('name'), 1)
	try:
		goods = paginator.page(page_num)
	except InvalidPage:
		goods = paginator.page(1)	
	return render(request, "index.html", {'category': cat, "cats": cats, "goods": goods})

def good(request, good_id):
	try:
		page_num = request.GET['page']
	except KeyError:
		page_num = 1
	cats = Category.objects.all().order_by("name")
	try:
		good = Good.objects.get(pk = good_id)
	except Good.DoesNotExist:
		raise Http404
	return render(request, 'good.html', {'cats': cats, 'good': good, 'pn': page_num})

