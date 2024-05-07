"""
This module contains URL patterns for the Django app.

The URLs module defines the routing configuration for the Django app, mapping URL patterns
to corresponding views or viewsets. It serves as the entry point for incoming HTTP requests
and dispatches them to the appropriate view functions or viewsets for processing.

Usage:
1. Define URL patterns using Django's URL patterns syntax.
2. Map URL patterns to views or viewsets using the `path` or `re_path` functions.
"""
from django.urls import path, include
from rest_framework import routers

from .views import (
    VendorViewSet,
    PurchaseOrderViewSet,
    VendorPerformanceAPIView,
    AcknowledgePurchaseOrderView,
    RecordHistoricalPerformanceView
)

router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendors')
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase_orders')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'vendors/<int:vendor_id>/performance',
        VendorPerformanceAPIView.as_view(),
        name='vendor_performance'
    ),
    path(
        'purchase_orders/<int:po_id>/acknowledge',
        AcknowledgePurchaseOrderView.as_view(),
        name='vendor_performance'
    ),
    path(
        'vendors/<int:vendor_id>/record_historical_performance',
        RecordHistoricalPerformanceView.as_view(),
        name='record_historical_performance'
    ),
]
