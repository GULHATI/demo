# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Technologies(models.Model):
    name = models.CharField(primary_key=True,max_length=500)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(primary_key=True,max_length=500)
    email = models.CharField(blank=True, null=True,max_length=500)
    phone = models.CharField(blank=True, null=True,max_length=500)
    pan =  models.CharField(blank=True, null=True,max_length=500)
    tan = models.CharField(blank=True, null=True,max_length=500)
    gst = models.CharField(blank=True, null=True,max_length=500)
    address = models.CharField(blank=True,null=True,max_length=3000)
    type = models.CharField(blank=True,null=True,max_length=3000)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(primary_key=True, max_length=500)
    email = models.CharField(blank=True, null=True, max_length=500)
    phone = models.CharField(blank=True, null=True, max_length=500)
    pan = models.CharField(blank=True, null=True, max_length=500)
    tan = models.CharField(blank=True, null=True, max_length=500)
    gst = models.CharField(blank=True, null=True, max_length=500)
    address = models.CharField(blank=True, null=True, max_length=3000)
    type = models.CharField(blank=True, null=True, max_length=3000)
    technologies = models.ManyToManyField(Technologies)

    def __str__(self):
        return self.name