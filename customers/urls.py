from django.urls import path
from . import views



urlpatterns = [
  path('<int:customer_id>/documents/', views.CustomerDocumentListAPIView.as_view()),
  path('<int:customer_id>/documents/<int:pk>/', views.DocumentDetailAPIView.as_view()),
  path('', views.CustomerListAPIView.as_view(), name='customers'),
  path('<int:id>', views.CustomeDetailAPIView.as_view()),
  path('documents', views.DocumentListAPIView.as_view(), name='customers'),
  path('documents/<int:id>', views.DocumentDetailAPIView.as_view()),

  # path('uploads/', views.DocumentAPIView.as_view()),

]