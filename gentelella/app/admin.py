from django.contrib import admin
from app.models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Register your models here.
admin.site.register(Articulo)
admin.site.register(Permission)
admin.site.register(ContentType)