from rest_framework import serializers
from .models import Asset, Document, NFCTag
from django.urls import reverse

class DocumentSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'document_type', 'uploaded_at', 'download_url']

    def get_download_url(self, obj):
        url = reverse('download_document', args=[obj.pk])
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url

class AssetSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = ['id', 'name', 'description', 'location', 'created_at', 'documents']