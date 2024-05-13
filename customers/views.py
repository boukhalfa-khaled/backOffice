from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  , ListAPIView
from rest_framework import  status 
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer,Document
from rest_framework import permissions
from .serializers import CustomerSerializer, DocumentSerializer



class CustomerListAPIView(ListCreateAPIView):
  serializer_class = CustomerSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Customer.objects.all()

  def perform_create(self, serializer):
    return serializer.save(created_by=self.request.user)

  # def get_queryset(self):
  #   return self.get_queryset
  

class CustomeDetailAPIView(RetrieveUpdateDestroyAPIView):
  serializer_class = CustomerSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Customer.objects.all()
  lookup_field = 'id'

  def get_queryset(self):
    return self.queryset


class DocumentListAPIView(ListCreateAPIView):
  serializer_class = DocumentSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Document.objects.all()

  # def perform_create(self, serializer):
  #   return serializer.save(created_by=self.request.user)

  # def get_queryset(self):
  #   return self.get_queryset
  

class DocumentDetailAPIView(RetrieveUpdateDestroyAPIView):
  serializer_class = DocumentSerializer
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Document.objects.all()
  lookup_field = 'id'

  def get_queryset(self):
      return self.queryset



class CustomerDocumentListAPIView(ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        queryset = Document.objects.filter(customer_id=customer_id)
        return queryset

  

# class DocumentAPIView(APIView):
#   serializer_class = DocumentSerializer
#   def get(self,request):
#     documents = Document.objects.all()
#     serializer = self.serializer_class(documents, many=True)  
#     return Response(serializer.data, status=status.HTTP_200_OK) 
