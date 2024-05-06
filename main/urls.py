"""
Manage main url paths here.
"""
from django.contrib import admin
from django.urls import path, include

from api.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('', index),
]
