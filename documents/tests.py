import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Asset, AuditLog, Document, NFCTag

TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class DocFlowTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username='radnik', password='test1234')
        self.asset = Asset.objects.create(name='Kompresor 1')
        NFCTag.objects.create(asset=self.asset, slug='kompresor-1')

    def make_doc(self, title='Uputstvo'):
        return Document.objects.create(
            asset=self.asset,
            title=title,
            file=SimpleUploadedFile('test.txt', b'sadrzaj'),
        )

    def test_profile_created_for_new_user(self):
        self.assertEqual(self.user.profile.role, 'worker')

    def test_new_version_replaces_old(self):
        v1 = self.make_doc()
        v2 = self.make_doc()
        v1.refresh_from_db()
        self.assertFalse(v1.is_current)
        self.assertTrue(v2.is_current)
        self.assertEqual(v2.version, 2)
        self.assertEqual(v2.previous_version, v1)

    def test_different_titles_are_separate_documents(self):
        a = self.make_doc('Uputstvo')
        b = self.make_doc('Garancija')
        a.refresh_from_db()
        self.assertTrue(a.is_current)
        self.assertTrue(b.is_current)
        self.assertEqual(b.version, 1)

    def test_audit_log_records_asset_creation(self):
        self.assertTrue(
            AuditLog.objects.filter(
                model_name='Asset', action='create', object_id=self.asset.pk
            ).exists()
        )

    def test_asset_page_requires_login(self):
        url = reverse('asset_detail', args=['kompresor-1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_asset_page_shows_only_current_versions(self):
        self.make_doc()
        self.make_doc()
        self.client.login(username='radnik', password='test1234')
        response = self.client.get(reverse('asset_detail', args=['kompresor-1']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['documents']), 1)

    def test_api_requires_login(self):
        response = self.client.get('/api/assets/')
        self.assertEqual(response.status_code, 403)

    def test_api_lists_assets_for_logged_in_user(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response = client.get('/api/assets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)