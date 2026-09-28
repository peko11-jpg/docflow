from django.contrib import admin
from .models import Asset, Document, NFCTag

admin.site.register(Asset)
admin.site.register(Document)
admin.site.register(NFCTag)