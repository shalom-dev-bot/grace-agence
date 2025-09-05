from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('create-event/', views.create_event_view, name='create_event'),
    path('event/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('event/<int:event_id>/add-service/', views.add_event_service_view, name='add_event_service'),
    path('event/<int:event_id>/update-invitation/', views.update_event_invitation_view, name='update_event_invitation'),

]