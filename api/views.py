from django.shortcuts import render
from rest_framework import viewsets, permissions, views, status, response
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone

from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from .models import Vendor, PurchaseOrder

class VendorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

def index(request):
    return render(request, 'api/index.html')

class VendorPerformanceAPIView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    def get(self, _, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            Vendor.calculate_metrics(vendor)  # Calculate metrics for the vendor
            serializer = VendorPerformanceSerializer(vendor)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return response.Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

class AcknowledgePurchaseOrderView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    def post(self, _, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Trigger recalculation of average_response_time
            Vendor.calculate_metrics(purchase_order.vendor)
            return response.Response({'message': 'Purchase order acknowledged successfully'}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return response.Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)
