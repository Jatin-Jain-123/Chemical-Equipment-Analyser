from django.urls import path
from .views import CSVUploadAPIView, DatasetListAPIView, LoginAPIView, DatasetPDFAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('upload/', CSVUploadAPIView.as_view(), name='csv-upload'),
    path('datasets/', DatasetListAPIView.as_view(), name='dataset-list'),
    path('datasets/<int:pk>/pdf/', DatasetPDFAPIView.as_view(), name='dataset-pdf'),
]