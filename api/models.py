"""
Django Models Module

The models module in Django provides an interface for defining, creating, querying, and manipulating
database tables in a Django application.
It allows developers to define data models as Python classes, where each class represents a database
table and each attribute represents a table column.

"""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Vendor(models.Model):
    """
    Class represents Vendor database model.
    
    Attributes:
        name: CharField - Vendor's name.
        contact_details: TextField - Contact information of the vendor.
        address: TextField - Physical address of the vendor.
        vendor_code: CharField - A unique identifier for the vendor.
        on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
        quality_rating_avg: FloatField - Average rating of quality based on purchase orders.
        average_response_time: FloatField - Average time taken to acknowledge purchase orders.
        fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.
    """
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=100)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return f"Vendor : {self.name}, code : {self.vendor_code}"

    @staticmethod
    def calculate_metrics(vendor):
        """
        Method to calculate on time delivery rate of a vendor.
        """
        if vendor:
            vendor_pos = PurchaseOrder.objects.filter(
                vendor=vendor
            )
            total_vendor_pos = vendor_pos.count()
            completed_pos = vendor_pos.filter(status='completed')
            total_completed_pos = completed_pos.count()
            if total_completed_pos == 0:
                vendor.on_time_delivery_rate = 0
            else:
                # Calculation for on time delivery rate.
                on_time_pos = completed_pos.filter(
                    delivery_date__gte=models.F('acknowledgment_date')
                ).count()
                on_time_delivery_rate = (on_time_pos / total_completed_pos) * 100
                vendor.on_time_delivery_rate = on_time_delivery_rate

            # Calculation for quality rating average.
            completed_pos_with_quality_rating = completed_pos.filter(
                quality_rating__isnull=False
            )
            total_completed_pos_with_quality_rating = completed_pos_with_quality_rating.count()
            if total_completed_pos_with_quality_rating > 0:
                quality_rating_sum = completed_pos_with_quality_rating.aggregate(
                    models.Sum('quality_rating')
                )['quality_rating__sum']
                quality_rating_avg = (
                    quality_rating_sum / total_completed_pos_with_quality_rating
                )
                vendor.quality_rating_avg = quality_rating_avg

            # Calculation for average response time.
            acknowledged_pos = vendor_pos.filter(
                acknowledgment_date__isnull=False
            )
            total_response_time = 0
            for po in acknowledged_pos:
                response_time = (po.acknowledgment_date - po.issue_date).total_seconds()
                total_response_time += response_time
            average_response_time = total_response_time / total_vendor_pos
            vendor.average_response_time = round(average_response_time, 2)

            # Calculation for fulfilment rate.
            fulfillment_rate = total_completed_pos / total_vendor_pos * 100
            vendor.fulfillment_rate = fulfillment_rate
            vendor.save()

class PurchaseOrder(models.Model):
    """
    Class represents Purchase Order database model.
    
    Attributes:
        po_number: CharField - Unique number identifying the PO.
        vendor: ForeignKey - Link to the Vendor model.
        order_date: DateTimeField - Date when the order was placed.
        delivery_date: DateTimeField - Expected or actual delivery date of the order.
        items: JSONField - Details of items ordered.
        quantity: IntegerField - Total quantity of items in the PO.
        status: CharField - Current status of the PO (e.g., pending, completed, canceled).
        quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
        issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
        acknowledgment_date: DateTimeField, nullable-Timestamp when the vendor acknowledged the PO.
    """
    po_number = models.CharField(unique=True, max_length=100, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    items = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, default='pending')
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"PO Number : {self.po_number}, Order Date : {self.order_date}"

@receiver(post_save, sender=PurchaseOrder)
def generate_po_number(sender, instance, created, **kwargs):
    """
    Method to generate po number for newly created purchase order.

    Args:
        sender (model class): Represents the class that sent the signal.
        instance (model instance): Represents the instance of the PurchaseOrder Model created.
        created (bool): Boolean flag represents whether the instance created or not.
    """
    if created and not instance.po_number:
        instance.po_number = f"PO-{instance.id:06d}"  # Pad ID with zeros to ensure minimum 6 digits
        instance.save()

@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    Vendor.calculate_metrics(instance.vendor)

class HistoricalPerformance(models.Model):
    """
    Class represents Historical Performance database model.
    
    Attributes:
        vendor: ForeignKey - Link to the Vendor model.
        date: DateTimeField - Date of the performance record.
        on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
        quality_rating_avg: FloatField - Historical record of the quality rating average.
        average_response_time: FloatField - Historical record of the average response
            time.
        fulfillment_rate: FloatField - Historical record of the fulfilment rate.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Vendor : {self.vendor.name}, Date : {self.date}"
