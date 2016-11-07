# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Category(models.Model):
	"""docstring for ClassName"""
	name = models.CharField(max_length = 30, unique = True)

	class Meta:
		verbose_name = 'Категории_'

	def __str__(self):
		# This method returns category name
		return self.name
	
@python_2_unicode_compatible
class Good(models.Model):
	name = models.CharField(max_length = 50, unique = True)
	description = models.TextField()
	in_stock = models.BooleanField(default = True, db_index = True)
	category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL)

	# Metadata for Good (additional options)
	class Meta:
		ordering = ['name']
		unique_together = ('category', 'name')
		verbose_name = 'Товары_'

	def get_is_stock(self):
		# If good in stock "+" or ""
		if self.in_stock:
			return "+"
		else:
			return ""

	def __str__(self):
		# This method returns good name and stock information
		s = self.name
		if not self.in_stock:
			s = s + " (not in stock)"
		return s