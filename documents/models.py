from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class NFCTag(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='nfc_tag')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"Tag za {self.asset.name}"


class Document(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title