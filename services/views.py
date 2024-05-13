from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  
from .models import Service
from rest_framework import permissions
from .serializers import ServiceSerializer



class ServiceListAPIView(ListCreateAPIView):
  serializer_class = ServiceSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Service.objects.all()


class ServiceDetailAPIView(RetrieveUpdateDestroyAPIView):
  serializer_class = ServiceSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Service.objects.all()
  lookup_field = 'id'

  def get_queryset(self):
    return self.queryset
