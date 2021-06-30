from django.contrib import admin

from .models import MaterialGroup, Material, Transaction

admin.site.register(MaterialGroup)
admin.site.register(Material)
admin.site.register(Transaction)
