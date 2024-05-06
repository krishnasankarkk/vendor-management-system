# Vendor Management System Documentation

Welcome to the Vendor Management System (VMS) documentation. This guide will help you set up and test the VMS system efficiently.

## Overview
The Vendor Management System (VMS) is a Django-based application developed to manage vendor profiles, track purchase orders, and calculate performance metrics for vendors. It offers comprehensive features for efficient vendor management.

## Features
### Vendor Profile Management
- Create, retrieve, update, and delete vendor profiles.
- Each profile includes essential information such as name, contact details, address, and a unique vendor code.

### Purchase Order Tracking
- Create, retrieve, update, and delete purchase orders.
- Track details of each purchase order including PO number, vendor reference, order date, items, quantity, and status.
- Filter purchase orders by vendor.

### Vendor Performance Evaluation
- Calculate performance metrics for vendors:
  - On-Time Delivery Rate
  - Quality Rating Average
  - Response Time
  - Fulfilment Rate

## Setup Instructions
Follow these steps to set up the Vendor Management System:

1. Clone the repository:
   ```
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```
   cd vendor_management_system
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```
6. Access the API at `http://localhost:8000/`.

## Testing
To test the functionality and reliability of the endpoints, follow these steps:

1. Run the test suite:
   ```
   python manage.py test
   ```
2. Check the test results for any failures and errors.

## API Endpoints
The VMS exposes the following API endpoints:

- **Vendor Profile Management:**
- `POST /api/vendors/`
- `GET /api/vendors/`
- `GET /api/vendors/{vendor_id}/`
- `PUT /api/vendors/{vendor_id}/`
- `DELETE /api/vendors/{vendor_id}/`

- **Purchase Order Tracking:**
- `POST /api/purchase_orders/`
- `GET /api/purchase_orders/`
- `GET /api/purchase_orders/{po_id}/`
- `PUT /api/purchase_orders/{po_id}/`
- `DELETE /api/purchase_orders/{po_id}/`

- **Vendor Performance Evaluation:**
- `GET /api/vendors/{vendor_id}/performance`

- **Additional Endpoints:**
- `POST /api/purchase_orders/{po_id}/acknowledge`

## Conclusion
The Vendor Management System provides a robust solution for tracking vendor profiles, purchase orders, and evaluating vendor performance metrics. If you encounter any issues during setup or testing, feel free to reach out for assistance.

Thank you for using the Vendor Management System!
