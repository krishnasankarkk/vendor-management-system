"""
This module contains view functions and viewsets for the Django app.

The views module defines the logic for processing HTTP requests and generating HTTP responses.
It contains view functions and viewsets that handle various operations, such as retrieving,
creating, updating, and deleting data, as well as rendering templates or serving API responses.

Usage:
1. Define view functions or viewsets to handle different HTTP methods (GET, POST, PUT, DELETE).
2. Implement business logic for processing data and generating responses.
3. Use serializers to serialize and deserialize data between views and models.
"""
from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions, response, status, views, viewsets
from rest_framework.authentication import TokenAuthentication

from .models import PurchaseOrder, Vendor, HistoricalPerformance
from .serializers import (
    PurchaseOrderSerializer,
    VendorPerformanceSerializer,
    VendorSerializer)


class VendorViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling CRUD operations on Vendor objects.

    This viewset provides endpoints for performing CRUD (Create, Retrieve, Update, Delete)
    operations on Vendor objects. It inherits from `ModelViewSet`, which automatically
    provides default implementations for standard actions like list, retrieve, create, 
    update, and destroy.

    Attributes:
    - authentication_classes: List of authentication classes used to authenticate users.
    - queryset: Queryset representing the collection of Vendor objects.
    - serializer_class: Serializer class used for serializing and deserializing Vendor objects.

    Usage:
    Define URL patterns and map them to this viewset using Django's URL patterns syntax.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling CRUD operations on Purchase Order objects.

    This viewset provides endpoints for performing CRUD (Create, Retrieve, Update, Delete)
    operations on Purchase Order objects. It inherits from `ModelViewSet`, which automatically
    provides default implementations for standard actions like list, retrieve, create, 
    update, and destroy.

    Attributes:
    - authentication_classes: List of authentication classes used to authenticate users.
    - queryset: Queryset representing the collection of Purchase Order objects.
    - serializer_class: Serializer class used for serializing and deserializing Purchase
        Order objects.

    Usage:
    Define URL patterns and map them to this viewset using Django's URL patterns syntax.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = self.queryset
        vendor_id = self.request.query_params.get('vendor_id', None)
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

def index(request):
    return render(request, 'api/index.html')

class VendorPerformanceAPIView(views.APIView):
    """
    API view for retrieving performance metrics of a specific vendor.

    This API view allows authenticated users to retrieve performance metrics for a specific vendor.
    The performance metrics include on-time delivery rate, quality rating average, average response
    time, and fulfillment rate. The metrics are calculated and serialized using the 
    VendorPerformanceSerializer.

    Attributes:
    - authentication_classes: List of authentication classes used to authenticate users.
    - permission_classes: List of permission classes controlling access to the view.

    Methods:
    - get: Handles HTTP GET requests and retrieves performance metrics for the specified vendor.

    Usage:
    Define URL patterns and map them to this view using Django's URL patterns syntax.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    def get(self, _, vendor_id):
        """
        Retrieve performance metrics for the specified vendor.

        This method handles HTTP GET requests and retrieves performance metrics for the vendor 
        with the specified ID. If the vendor is found, metrics are calculated and serialized 
        using the VendorPerformanceSerializer. If the vendor does not exist, a 404 error 
        response is returned.

        Parameters:
        - request: HTTP request object.
        - vendor_id: ID of the vendor to retrieve performance metrics for.

        Returns:
        - Response with performance metrics data and HTTP status code.

        """
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            Vendor.calculate_metrics(vendor)  # Calculate metrics for the vendor
            serializer = VendorPerformanceSerializer(vendor)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return response.Response(
                {'error': 'Vendor not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class AcknowledgePurchaseOrderView(views.APIView):
    """
    API view for acknowledging a purchase order.

    This API view allows authenticated users to acknowledge a purchase order by updating its
    acknowledgment date. Upon acknowledgment, the average response time for the vendor associated
    with the purchase order is recalculated.

    Attributes:
    - authentication_classes: List of authentication classes used to authenticate users.
    - permission_classes: List of permission classes controlling access to the view.

    Methods:
    - post: Handles HTTP POST requests and acknowledges the specified purchase order.

    Usage:
        Define URL patterns and map them to this view using Django's URL patterns syntax.
    Permissions:
        By default, this view requires authentication by token, ensuring that only users with a 
        valid token can access it.
        You can further customize permissions by setting appropriate permission classes using 
        the `permission_classes` attribute.

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    def post(self, _, po_id):
        """
        Acknowledge the specified purchase order.

        This method handles HTTP POST requests and acknowledges the purchase order with the 
        specified ID. Upon acknowledgment, the acknowledgment date of the purchase order is
        updated to the current timestamp. Additionally, the average response time for the 
        vendor associated with the purchase order is recalculated.

        Parameters:
        - request: HTTP request object.
        - po_id: ID of the purchase order to acknowledge.

        Returns:
        - Response with acknowledgment status message and HTTP status code.
        
        """
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Trigger recalculation of average_response_time
            Vendor.calculate_metrics(purchase_order.vendor)
            return response.Response(
                {'message': 'Purchase order acknowledged successfully'},
                status=status.HTTP_200_OK
            )
        except PurchaseOrder.DoesNotExist:
            return response.Response(
                {'error': 'Purchase order not found!'},
                status=status.HTTP_404_NOT_FOUND
            )
class RecordHistoricalPerformanceView(views.APIView):
    """
    API view for record historical performance of vendor.

    This API view allows authenticated users to record the historical performance of a vendor.

    Attributes:
    - authentication_classes: List of authentication classes used to authenticate users.
    - permission_classes: List of permission classes controlling access to the view.

    Methods:
    - post: Handles HTTP POST requests and record the historical performance of specified vendor.

    Usage:
        Define URL patterns and map them to this view using Django's URL patterns syntax.
    Permissions:
        By default, this view requires authentication by token, ensuring that only users with a 
        valid token can access it.
        You can further customize permissions by setting appropriate permission classes using 
        the `permission_classes` attribute.

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    def post(self, _, vendor_id):
        """
        Record historical performance of the specified vendor.

        This method handles HTTP POST requests and record the historical performance of a vendor.

        Parameters:
        - request: HTTP request object.
        - vendor_id: ID of the given vendor.

        Returns:
        - Response with message and HTTP status code.
        
        """
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            record = HistoricalPerformance()
            record.vendor = vendor
            record.save()
            return response.Response(
                {'message': 'Recorded performance of vendor successfully'},
                status=status.HTTP_200_OK
            )
        except Vendor.DoesNotExist:
            return response.Response(
                {'error': 'Vendor not found!'},
                status=status.HTTP_404_NOT_FOUND
            )
