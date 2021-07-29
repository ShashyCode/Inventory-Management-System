from django.contrib import admin
from home.models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(Locations, Product, ProductMovement)
class ViewAdmin(ImportExportModelAdmin):
    pass