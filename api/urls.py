from django.urls import path, include
from rest_framework import routers

from .views import VendorViewSet, PurchaseOrderViewSet, VendorPerformanceAPIView, AcknowledgePurchaseOrderView

router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

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
]
