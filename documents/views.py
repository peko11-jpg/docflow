from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NFCTag, Asset, Document
from .serializers import AssetSerializer, DocumentSerializer
from rest_framework import viewsets, permissions, filters
import os
import mimetypes
from django.http import FileResponse, Http404


@login_required
def asset_detail(request, slug):
    tag = get_object_or_404(NFCTag, slug=slug)
    asset = tag.asset
    documents = asset.documents.filter(is_current=True)
    return render(request, 'documents/asset_detail.html', {
        'asset': asset,
        'documents': documents,
    })

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'location']


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'document_type']

INLINE_TYPES = {
    'application/pdf', 'image/png', 'image/jpeg', 'image/gif', 'image/webp',
}


@login_required
def download_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    content_type, _ = mimetypes.guess_type(doc.file.name)
    try:
        return FileResponse(
            doc.file.open('rb'),
            as_attachment=content_type not in INLINE_TYPES,
            filename=os.path.basename(doc.file.name),
        )
    except FileNotFoundError:
        raise Http404("Fajl ne postoji.")