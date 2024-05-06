"""
This module contains tests for the Django app.

The test module provides unit tests, integration tests, and functional tests to ensure the proper
functioning of the Django app's components, including models, views, serializers, and API endpoints.


Usage:
1. Run the test suite using the Django test runner:
   ```
   python manage.py test
   ```
"""
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Vendor, PurchaseOrder

class VendorAPITest(TestCase):
    """
    Test suite for the Vendor API endpoints.

    This class contains test cases for the Vendor API endpoints to ensure their
    functionality and reliability.

    Attributes:
        client: APIClient instance for making HTTP requests to the API endpoints.
        vendor: Vendor instance created for testing purposes.
    """
    def setUp(self):
        """
        Set up preconditions for the test cases.

        This method is called before each test case to set up any necessary preconditions,
        such as creating instances of models or initializing test data.
        """
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )
        # Create a user and obtain their authentication token
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.token = Token.objects.create(user=self.user)

        # Set authentication for all requests made using self.client
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_vendors(self):
        """
        Test the list vendors endpoint.

        This method sends a GET request to the list vendors endpoint and asserts that
        the response status code is HTTP 200 OK.
        """
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vendor(self):
        """
        Test the retrieve vendor endpoint.

        This method sends a GET request to the retrieve vendor endpoint and asserts that
        the response status code is HTTP 200 OK.
        """
        response = self.client.get(f'/api/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        """
        Test the create vendor endpoint.

        This method sends a POST request to the create vendor endpoint and asserts that
        the response status code is HTTP 200 OK.
        """
        data = {
            'name': 'New Vendor',
            'contact_details': 'new_vendor@example.com',
            'address': '456 New St',
            'vendor_code': 'NEW123'
        }
        response = self.client.post('/api/vendors/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_vendor(self):
        """
        Test the update vendor endpoint.

        This method sends a PUT request to the update vendor endpoint and asserts that
        the response status code is HTTP 200 OK.
        """
        data = {
            'name': 'Update Vendor',
            'contact_details': 'update_vendor@example.com',
            'address': '456 Update St',
            'vendor_code': 'Update123'
        }
        response = self.client.put(f'/api/vendors/{self.vendor.id}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        """
        Test the delete vendor endpoint.

        This method sends a PUT request to the delete vendor endpoint and asserts that
        the response status code is HTTP 200 OK.
        """
        response = self.client.delete(f'/api/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class PurchaseOrderAPITest(TestCase):
    """
    Test suite for the Purchase Order API endpoints.

    This class contains test cases for the Purchase Order API endpoints to ensure their
    functionality and reliability.

    Attributes:
        client: APIClient instance for making HTTP requests to the API endpoints.
        vendor: Vendor instance created for testing purposes.
        po: Purchase Order instance created for testing purposes.
    """
    def setUp(self):
        """
        Set up preconditions for the test cases.

        This method is called before each test case to set up any necessary preconditions,
        such as creating instances of models or initializing test data.
        """
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST123'
        )
        self.vendor1 = Vendor.objects.create(
            name='Test Vendor 1',
            contact_details='test@example.com',
            address='123 Test St',
            vendor_code='TEST1234'
        )
        self.po = PurchaseOrder.objects.create(
            vendor=self.vendor
        )
        self.po1 = PurchaseOrder.objects.create(
            vendor=self.vendor1
        )

    def test_list_purchase_orders(self):
        """
        Test the list purchase orders endpoint.

        This method sends a GET request to the list purchase order endpoint and asserts that
        the response status code is HTTP 200 OK.
        """
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_purchase_orders_filter_by_vendor(self):
        """
        Test the list purchase orders endpoint.

        This method sends a GET request to the list purchase order endpoint and asserts that
        the response status code is HTTP 200 OK.
        """
        response = self.client.get(f'/api/purchase_orders/?vendor_id={self.vendor.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_purchase_order(self):
        """
        Test the retrieve purchase order endpoint.

        This method sends a GET request to the retrieve purchase order endpoint with a valid po ID
        and asserts that the response status code is HTTP 200 OK.
        """
        response = self.client.get(f'/api/purchase_orders/{self.po.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
