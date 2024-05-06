"""
This module provides an administrative interface for managing the data of the Django app.

The admin module allows administrators to perform CRUD (Create, Read, Update, Delete) operations
on the app's data without writing custom views or forms.

To access the admin interface, navigate to the admin URL of the Django app and log in with
administrator credentials.

"""
from django.contrib import admin

from . import models

admin.site.register(models.Vendor)
admin.site.register(models.PurchaseOrder)
admin.site.register(models.HistoricalPerformance)
