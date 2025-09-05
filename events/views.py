from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .models import Event, EventType, InvitationCard
from services.models import Service
from testimonials.models import Testimonial

def home_view(request):
    # Get featured testimonials
    featured_testimonials = Testimonial.objects.filter(
        is_approved=True, is_featured=True
    ).select_related('user')[:6]
    
    # Get recent events count
    recent_events_count = Event.objects.filter(status='completed').count()
    
    # Get available services count
    services_count = Service.objects.filter(is_active=True).count()
    
    context = {
        'featured_testimonials': featured_testimonials,
        'recent_events_count': recent_events_count,
        'services_count': services_count,
    }
    return render(request, 'events/home.html', context)

@login_required
def dashboard_view(request):
    user_events = Event.objects.filter(user=request.user)
    recent_events = user_events[:5]
    
    context = {
        'recent_events': recent_events,
        'total_events': user_events.count(),
        'completed_events': user_events.filter(status='completed').count(),
        'upcoming_events': user_events.filter(status__in=['planning', 'confirmed']).count(),
    }
    return render(request, 'events/dashboard.html', context)

@login_required
def create_event_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type_id = request.POST.get('event_type')
        event_date = request.POST.get('event_date')
        location = request.POST.get('location')
        guest_count = request.POST.get('guest_count', 0)
        budget = request.POST.get('budget')
        
        if title and event_type_id and event_date:
            event_type = get_object_or_404(EventType, id=event_type_id)
            event = Event.objects.create(
                user=request.user,
                title=title,
                description=description,
                event_type=event_type,
                event_date=event_date,
                location=location,
                guest_count=int(guest_count) if guest_count else 0,
                budget=float(budget) if budget else None,
            )
            messages.success(request, _('Event created successfully!'))
            return redirect('event_detail', event_id=event.id)
        else:
            messages.error(request, _('Please fill in all required fields.'))
    
    event_types = EventType.objects.all()
    return render(request, 'events/create_event.html', {'event_types': event_types})

@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    available_services = Service.objects.filter(is_active=True)
    invitation_cards = InvitationCard.objects.filter(is_active=True)
    
    context = {
        'event': event,
        'available_services': available_services,
        'invitation_cards': invitation_cards,
    }
    return render(request, 'events/event_detail.html', context)

def gallery_view(request):
    # Display completed events as gallery
    completed_events = Event.objects.filter(
        status='completed'
    ).select_related('user', 'event_type')
    
    paginator = Paginator(completed_events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events/gallery.html', {'page_obj': page_obj})

@login_required
def add_event_service_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        service_id = request.POST.get('service')
        quantity = request.POST.get('quantity')
        notes = request.POST.get('notes')
        if service_id and quantity:
            service = get_object_or_404(Service, id=service_id)
            EventService.objects.create(
                event=event,
                service=service,
                quantity=int(quantity),
                notes=notes
            )
            messages.success(request, _('Service added successfully!'))
        else:
            messages.error(request, _('Please select a service and specify a quantity.'))
    return redirect('event_detail', event_id=event.id)

@login_required
def update_event_invitation_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        invitation_card_id = request.POST.get('invitation_card')
        if invitation_card_id:
            invitation_card = get_object_or_404(InvitationCard, id=invitation_card_id)
            event.invitation_card = invitation_card
        else:
            event.invitation_card = None
        event.save()
        messages.success(request, _('Invitation card updated successfully!'))
    return redirect('event_detail', event_id=event.id)