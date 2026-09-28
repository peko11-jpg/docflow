from django.urls import path
from . import views

urlpatterns = [
    path('asset/<slug:slug>/', views.asset_detail, name='asset_detail'),
]