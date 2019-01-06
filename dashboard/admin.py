# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Customer, Technologies, Supplier, TempFile, RFQ

admin.site.register(Customer)
admin.site.register(Technologies)
admin.site.register(Supplier)
admin.site.register(TempFile)
admin.site.register(RFQ)

# Register your models here.
