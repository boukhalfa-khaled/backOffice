from rest_framework import serializers
from .models import Invoice
from users.serializers import UsersSerializer
from customers.serializers import CustomerSerializer
from services.serializers import ServiceSerializer

class  InvoiceSerializer(serializers.ModelSerializer):
  created = UsersSerializer(read_only=True)
  customer = CustomerSerializer(read_only=True)
  service = ServiceSerializer(read_only=True)
  class Meta:
    model = Invoice
    fields = '__all__' 
    fields = ['id', 'title', 'description', 'status', 'price', 'qty',  'total', 'created_at', 'update_at', 'service_id', 'customer_id', 'created_by', 'created', 'customer', 'service']
    depth =  1