from django.urls import path
from .views import  RegisterView, VerifyEmail, LoginApiView, PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView, LogoutAPIView, ProfileAPIView, CustomTokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView
# , LoginView, UserView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>', PasswordTokenCheckAPI.as_view(), name='password-rest-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
