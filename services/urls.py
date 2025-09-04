from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_list_view, name='services_list'),
    path('<int:service_id>/', views.service_detail_view, name='service_detail'),
]