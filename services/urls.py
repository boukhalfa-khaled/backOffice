from django.urls import path
from . import views



urlpatterns = [
  path('', views.ServiceListAPIView.as_view(), name='services'),
  path('<int:id>', views.ServiceDetailAPIView.as_view(), name='service'),
]