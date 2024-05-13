from rest_framework import generics , status , views
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .utils import Util
from .models import User
from .serializers import RegisterSerializer, EmailVerificationSerializer ,LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, LogoutSerializer, ProfileSerializer, UsersSerializer
from django.conf import settings
from django.shortcuts import redirect
import os



class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user =request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            domain = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absURL = 'http://'+domain+relativeLink+"?token="+str(token)
            # absURL = f'http://{domain}{relativeLink}?token={token}'
            email_body = 'Hi '+user.name + \
            ' Use the link below to verify your email \n'+absURL
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject':  'Verify Your Email'}
            Util.send_email(data)
            return Response(user_data,status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            error_messages = []
            for field, messages in errors.items():
                for message in messages:
                    error_messages.append({"field": field, "message": message})
            return Response({"errors": error_messages}, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'] )
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return redirect(os.environ.get('FRONTEND_URL', '') + 'auth/signin' + '?message=Acount Succesfully Activated Please Login to Proced' )
                # return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            return Response({'email': 'Account Already activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response()
        refresh_token = serializer.context.get('refresh_token')
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.status = status.HTTP_200_OK
        response.data = serializer.data
        return response



class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            domain = get_current_site(request=request).domain
            relativeLink = reverse('password-rest-confirm', kwargs={'uidb64':uidb64, 'token':token})
            absURL = 'http://'+domain+relativeLink
            # absURL = f'http://{domain}{relativeLink}?token={token}'
            redirect_url= request.data.get('redirect_url', '')
            email_body = 'Hello, \n Use the link below to reset your password \n'+absURL
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject':  'Reset Your Password'}
            Util.send_email(data)
        return Response({'success':'We Have Send you a Link To Reset Your Password'},status=status.HTTP_200_OK)



class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self,request, uidb64, token):
        # redirect_url=request.GET.get('redirect_url')
        #  redirect_url=os.environ.get('FRONTEND_URL', '')

        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                # if len(redirect_url)>3:
                    # return redirect(redirect_url+'?token_valid=False')
                return redirect(os.environ.get('FRONTEND_URL', '')+ 'auth/signin' +'?error=Something Went Wrong')


            return redirect(os.environ.get('FRONTEND_URL', '') + 'auth/new-password' + '?uidb64=' + uidb64 + '&token=' + token)
            # return redirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=True&?message=CredentialsValid&?uidb64='+uidb64+'&?token='+token)

                # return Response({'error', 'Token is not validl please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
            # return Response({'success':True, 'message':'Credentials Valide','uidb64':uidb64, 'token':token }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
                return redirect(os.environ.get('FRONTEND_URL', '')+ 'auth/signin' +'?error=Link Expired Please Request A New One')
                # return Response({'error', 'Token is not validl please request a new one'},status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class= SetNewPasswordSerializer
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password Reset Success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    def post (self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed('Refresh Toekn not found.')

        serializer = self.serializer_class(data={'refresh_token':refresh_token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.delete_cookie(key="refresh_token")
        response.set_cookie(key='refresh_token', value="khaled", httponly=True)
        response.status = status.HTTP_204_NO_CONTENT
        response.data = {'success' : 'you logout successfully'}
        return response

class ProfileAPIView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class UserAPIView(generics.RetrieveAPIView):
#     queryset = User.objects.all()  
#     serializer_class = UsersSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     lookup_field  = 'id'



# class UsersAPIView(generics.GenericAPIView):
#     serializer_class = UsersSerializer
#     permission_classes = (permissions.IsAuthenticated,)
    # def get(self, request):
    #     users = User.objects.all()  
    #     serializer = self.serializer_class(users, many=True)  
    #     return Response(serializer.data, status=status.HTTP_200_OK) 

    



class CustomTokenRefreshView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({'detail': 'Missing refresh token in cookie.'}, status=status.HTTP_400_BAD_REQUEST)

            token_obj = RefreshToken(refresh_token)
            access_token =   str(token_obj.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except RefreshToken.InvalidToken:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)




class UsersListAPIView(ListCreateAPIView):
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()


class UsersDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset

