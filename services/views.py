from django.shortcuts import render
from .models import Service, ServiceCategory

def services_list_view(request):
    categories = ServiceCategory.objects.prefetch_related('services').all()
    featured_services = Service.objects.filter(is_active=True, is_featured=True)
    
    context = {
        'categories': categories,
        'featured_services': featured_services,
    }
    return render(request, 'services/services_list.html', context)