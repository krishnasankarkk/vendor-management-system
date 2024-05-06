"""
This module provides serializers for converting Django model instances into JSON representations.

Serializers define the API representation of Django models, specifying which fields should be
included in the serialized output and how they should be formatted.

"""
from rest_framework import serializers

from .models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer for converting Vendor model instances into JSON representations.

    This serializer defines the API representation of Vendor model instances, specifying which
    fields should be included in the serialized output and how they should be formatted.

    Fields:
    - id: Unique identifier for the vendor.
    - name: Name of the vendor.
    - contact_details: Contact information of the vendor.
    - address: Physical address of the vendor.
    - vendor_code: A unique identifier for the vendor.
    - on_time_delivery_rate: Percentage of on-time deliveries by the vendor.
    - quality_rating_avg: Average rating of quality based on purchase orders from the vendor.
    - average_response_time: Average time taken by the vendor to acknowledge purchase orders.
    - fulfillment_rate: Percentage of purchase orders fulfilled successfully by the vendor.

    """
    class Meta:
        """
        Meta Options:
        - model: The Django model class that the serializer is based on.
        - fields: The fields to include in the serialized output.

        """
        model = Vendor
        fields = [
            'id',
            'name',
            'contact_details',
            'address',
            'vendor_code',
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate'
        ]

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for converting PurchaseOrder model instances into JSON representations.

    This serializer defines the API representation of PurchaseOrder model instances, specifying
    which fields should be included in the serialized output and how they should be formatted.
  
    Fields:
    - id: Unique identifier for the purchase order.
    - po_number: Unique number identifying the purchase order.
    - vendor: Link to the vendor associated with the purchase order.
    - order_date: Date when the purchase order was placed.
    - delivery_date: Expected or actual delivery date of the purchase order.
    - items: Details of items ordered in JSON format.
    - quantity: Total quantity of items in the purchase order.
    - status: Current status of the purchase order (e.g., pending, completed, canceled).
    - quality_rating: Rating given to the vendor for this purchase order (nullable).
    - issue_date: Timestamp when the purchase order was issued to the vendor.
    - acknowledgment_date: Timestamp when the vendor acknowledged the purchase order (nullable).

    """
    class Meta:
        """
        Meta Options:
        - model: The Django model class that the serializer is based on.
        - fields: The fields to include in the serialized output.

        """
        model = PurchaseOrder
        fields = [
            'id',
            'po_number',
            'vendor',
            'order_date',
            'delivery_date',
            'items',
            'quantity',
            'status',
            'quality_rating',
            'issue_date',
            'acknowledgment_date'
        ]

class VendorPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for calculating and representing performance metrics of Vendor model instances.

    This serializer calculates and represents performance metrics of Vendor model instances,
    including on-time delivery rate, quality rating average, average response time, and
    fulfillment rate.

    Fields:
    - on_time_delivery_rate: Percentage of on-time deliveries by the vendor.
    - quality_rating_avg: Average rating of quality based on purchase orders from the vendor.
    - average_response_time: Average time taken by the vendor to acknowledge purchase orders.
    - fulfillment_rate: Percentage of purchase orders fulfilled successfully by the vendor.
    """
    class Meta:
        """
        Meta Options:
        - model: The Django model class that the serializer is based on.
        - fields: The fields to include in the serialized output.

        """
        model = Vendor
        fields = [
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate'
        ]
