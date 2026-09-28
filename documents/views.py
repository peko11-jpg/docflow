from django.shortcuts import render, get_object_or_404
from .models import NFCTag

def asset_detail(request, slug):
    tag = get_object_or_404(NFCTag, slug=slug)
    asset = tag.asset
    documents = asset.documents.all()
    return render(request, 'documents/asset_detail.html', {
        'asset': asset,
        'documents': documents,
    })