#!/usr/bin/env python
from variables.models import Variable
from django.contrib import admin


class VariableAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ('name', 'value')


admin.site.register(Variable, VariableAdmin)