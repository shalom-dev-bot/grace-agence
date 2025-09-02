from django.urls import path
from . import views

urlpatterns = [
    path('', views.testimonials_list_view, name='testimonials_list'),
    path('add/', views.add_testimonial_view, name='add_testimonial'),
]