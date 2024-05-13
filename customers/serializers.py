from rest_framework import serializers
from .models import Customer, Document

class  CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ['id', 'name', 'description', 'email', 'phone', 'address', 'date', 'created_by']



class DocumentSerializer(serializers.ModelSerializer):
  file_size = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = Document
    fields = '__all__' 

  def get_file_size(self, obj):
      if obj.file:
          return obj.file.size
      return None