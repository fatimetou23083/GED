from django.contrib import admin
from .models import Document, DocumentVersion, Metadata, SearchIndex

admin.site.register(Document)
admin.site.register(DocumentVersion)
admin.site.register(Metadata)
admin.site.register(SearchIndex)
