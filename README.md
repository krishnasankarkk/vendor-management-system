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

1. Ensure latest python and pip is installed.
   ```
   python --version && pip --version
   ```
2. Setup virtual environment for the project.
   ```
   python -m venv venv
   ```
3. Activate virtual environment.
   
    On Windows:
     ```
     venv\Scripts\activate
     ```
    On Linux:
     ```
     source venv/bin/activate
     ```
4. Clone the repository:
   ```
   git clone https://github.com/krishnasankarkk/vendor-management-system.git
   ```
5. Navigate to the project directory:
   ```
   cd vendor-management-system
   ```
6. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
7. Apply migrations:
   ```
   python manage.py migrate
   ```
8. Run the development server:
   ```
   python manage.py runserver
   ```
9. Access the API at `http://localhost:8000/api/`.

## API Endpoints
The VMS exposes the following API endpoints:

- **Vendor Profile Management:**
  - `POST /api/vendors/` : Create a new vendor.
  - `GET /api/vendors/` : List all vendors.
  - `GET /api/vendors/{vendor_id}/` : Retrieve a specific vendor's details.
  - `PUT /api/vendors/{vendor_id}/` : Update a vendor's details.
  - `DELETE /api/vendors/{vendor_id}/` : Delete a vendor.

- **Purchase Order Tracking:**
  - `POST /api/purchase_orders/` : Create a purchase order.
  - `GET /api/purchase_orders/` : List all purchase orders with an option to filter by
vendor.
  - `GET /api/purchase_orders/{po_id}/` : Retrieve details of a specific purchase order.
  - `PUT /api/purchase_orders/{po_id}/` : Update a purchase order.
  - `DELETE /api/purchase_orders/{po_id}/` : Delete a purchase order.

- **Vendor Performance Evaluation:**
  - `GET /api/vendors/{vendor_id}/performance` : Retrieve a vendor's performance
metrics.

- **Additional Endpoints:**
  - `POST /api/purchase_orders/{po_id}/acknowledge` : For vendors to acknowledge
POs.

## Testing
To test the functionality and reliability of the endpoints, follow these steps:

1. Run the test suite:
   ```
   python manage.py test
   ```
2. Check the test results for any failures and errors.

## Conclusion
The Vendor Management System provides a robust solution for tracking vendor profiles, purchase orders, and evaluating vendor performance metrics. If you encounter any issues during setup or testing, feel free to reach out for assistance.

Thank you for using the Vendor Management System!
