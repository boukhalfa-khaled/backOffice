from rest_framework import  status  
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.serializers import TokenRefreshSerializer



from .models import User




class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(min_length=6, write_only=True) 

  class Meta:
    model = User
    fields = ['name', 'email', 'password']
  
  def validate(self, attrs):
      email = attrs.get('email')
      password = attrs.get('password')

      if User.objects.filter(email=email).exists():
          raise serializers.ValidationError("Email address llllll already exists", status=status.HTTP_403_FORBIDDEN)

      if len(password) < 8:
          raise serializers.ValidationError("Password is too short")

      return attrs

  def create(self, validated_data):
      password = validated_data.pop('password', None)
      user = self.Meta.model(**validated_data, is_active=True, is_verified=False)
      if password is not None:
        user.set_password(password)
      user.save()
      return user 



class LoginSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=255, read_only=True)
  email= serializers.EmailField(max_length=255, min_length=3)
  password= serializers.CharField(max_length=568,min_length=6, write_only=True)
  token= serializers.CharField(max_length=255, read_only=True)

  class Meta:
    model = User
    fields = ['email', 'password', 'token', 'name']

  def validate(self, attrs):
    email= attrs.get('email', '')
    password = attrs.get('password', '')
    user = authenticate(email=email, password=password)
    if not user:
      raise AuthenticationFailed('Invalide creadentials, try again')
    if not user.is_active:
      raise AuthenticationFailed('Account disabled, contact admin')
    if not user.is_verified:
      raise AuthenticationFailed('email is not verified')
    
    tokens = user.tokens()
    refresh_token = tokens['refresh']
    token = tokens['access']

    self.context['refresh_token'] = refresh_token
    return {
      'name': user.name,
      'email': user.email,
      'token': token
    }



class ResetPasswordEmailRequestSerializer(serializers.Serializer):
  email=serializers.EmailField(min_length=2)
  redirect_url = serializers.CharField(max_length=500, required=False)
  class Meta:
    fields= ['email']


class SetNewPasswordSerializer(serializers.Serializer):
  password=serializers.CharField(min_length=6, max_length=68, write_only=True)
  token=serializers.CharField(min_length=1, write_only=True)
  uidb64=serializers.CharField(min_length=1, write_only=True)

  class Meta:
    fields = ['password', 'token' ,'uidb64']
  def validate(self, attrs):
    try:
      password=attrs.get('password','')
      token=attrs.get('token','')
      uidb64=attrs.get('uidb64','')

      id = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise AuthenticationFailed('The Reset Link Is Invalide', 401)
      user.set_password(password)
      user.save()
      return attrs
    except Exception as e:
        raise AuthenticationFailed('The Reset Link Is Invalide', 401)


class LogoutSerializer(serializers.Serializer):
  refresh_token = serializers.CharField(required=False)
  default_error_messages = {
      'bad_token': ('Token is expired or invalid')
  }


  def validate(self, attrs):
    self.refresh_token = attrs.get('refresh_token')
    return attrs

  def save(self, **kwargs):
    try:
      RefreshToken(self.refresh_token).blacklist()
    except TokenError:
      self.fail('bad_token')


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email']

