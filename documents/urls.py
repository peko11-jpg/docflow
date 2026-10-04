from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assets', views.AssetViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = [
    path('asset/<slug:slug>/', views.asset_detail, name='asset_detail'),
    path('api/', include(router.urls)),
]