from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory

def services_list_view(request):
    category_filter = request.GET.get('category', '')
    categories = ServiceCategory.objects.prefetch_related('services').all()
    featured_services = Service.objects.filter(is_active=True, is_featured=True)
    
    if category_filter:
        categories = categories.filter(id=category_filter)
    
    context = {
        'categories': categories,
        'featured_services': featured_services,
        'category_filter': category_filter,
    }
    return render(request, 'services/services_list.html', context)

def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    context = {'service': service}
    return render(request, 'services/service_detail.html', context)