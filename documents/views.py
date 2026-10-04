from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NFCTag, Asset, Document
from .serializers import AssetSerializer, DocumentSerializer
from rest_framework import viewsets, permissions


@login_required
def asset_detail(request, slug):
    tag = get_object_or_404(NFCTag, slug=slug)
    asset = tag.asset
    documents = asset.documents.all()
    return render(request, 'documents/asset_detail.html', {
        'asset': asset,
        'documents': documents,
    })

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]