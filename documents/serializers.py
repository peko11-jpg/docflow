from rest_framework import serializers
from .models import Asset, Document, NFCTag

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'document_type', 'uploaded_at']


class AssetSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = ['id', 'name', 'description', 'location', 'created_at', 'documents']