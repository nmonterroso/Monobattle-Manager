#!/usr/bin/env python
from viewers.models import Viewer, ViewerSubmission
from django.contrib import admin

admin.site.register(Viewer)
admin.site.register(ViewerSubmission)