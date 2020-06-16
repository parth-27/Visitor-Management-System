# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.
@admin.register(User)
class ViewAdmin(ImportExportActionModelAdmin):
    pass
