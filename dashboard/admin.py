# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Customer,Technologies,Supplier

admin.site.register(Customer)
admin.site.register(Technologies)
admin.site.register(Supplier)

# Register your models here.
