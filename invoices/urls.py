from django.urls import path
from . import views



urlpatterns = [
  path('', views.InvoiceListAPIView.as_view(), name='invoices'),
  path('<int:id>', views.InvoiceDetailAPIView.as_view(), name='invoice'),
]