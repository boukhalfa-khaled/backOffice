from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  
from .models import Invoice
from customers.models import Customer
from services.models import Service
from rest_framework import permissions
from .serializers import InvoiceSerializer



class InvoiceListAPIView(ListCreateAPIView):
  serializer_class = InvoiceSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Invoice.objects.all()

  def perform_create(self, serializer):
        customer_id = self.request.data.get('customer_id')
        service_id = self.request.data.get('service_id')

        customer = Customer.objects.get(pk=customer_id)
        service = Service.objects.get(pk=service_id)
        # Assign the user making the request
        return serializer.save(customer_id=customer, service_id=service, created_by=self.request.user)



class InvoiceDetailAPIView(RetrieveUpdateDestroyAPIView):
  serializer_class = InvoiceSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Invoice.objects.all()
  lookup_field = 'id'

  def get_queryset(self):
    return self.queryset
