from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete

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
    version = models.PositiveIntegerField(default=1)
    previous_version = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='next_versions'
    )
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} (v{self.version})"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('worker', 'Radnik'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='worker')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


def log_action(sender, instance, action, **kwargs):
    AuditLog.objects.create(
        action=action,
        model_name=sender.__name__,
        object_id=instance.pk,
        object_repr=str(instance),
    )

@receiver(post_save, sender=Asset)
def log_asset_save(sender, instance, created, **kwargs):
    log_action(sender, instance, 'create' if created else 'update')

@receiver(post_delete, sender=Asset)
def log_asset_delete(sender, instance, **kwargs):
    log_action(sender, instance, 'delete')

@receiver(post_save, sender=Document)
def log_document_save(sender, instance, created, **kwargs):
    log_action(sender, instance, 'create' if created else 'update')

@receiver(post_delete, sender=Document)
def log_document_delete(sender, instance, **kwargs):
    log_action(sender, instance, 'delete')


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Kreirano'),
        ('update', 'Izmenjeno'),
        ('delete', 'Obrisano'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} #{self.object_id}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

