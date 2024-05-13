from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
# , LoginView, UserView, LogoutView

urlpatterns = [
    path('<id>',views.UsersDetailAPIView.as_view(), name='users'),
    path('', views.UsersListAPIView.as_view(), name='users'),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>', views.PasswordTokenCheckAPI.as_view(), name='password-rest-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
]
