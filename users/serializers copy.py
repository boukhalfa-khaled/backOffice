from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'name', 'email', 'password']
    extra_kwargs = {
      'password': {'write_only':True}
    }

  def validate(self, attrs):
      email = attrs.get('email')
      password = attrs.get('password')

      if User.objects.filter(email=email).exists():
          raise serializers.ValidationError("Email address already exists")

      if len(password) < 8:
          raise serializers.ValidationError("Password is too short")

      return attrs

  def create(self, validated_data):
    password = validated_data.pop('password', None)
    user = self.Meta.model(**validated_data, is_active=False)
    if password is not None:
      user.set_password(password)
    user.save()
    return user 
