from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .models import Testimonial
from .forms import TestimonialForm

def testimonials_list_view(request):
    testimonials = Testimonial.objects.filter(is_approved=True).select_related('user')
    
    paginator = Paginator(testimonials, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'testimonials/testimonials_list.html', {'page_obj': page_obj})

@login_required
def add_testimonial_view(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, _('Thank you for your testimonial! It will be reviewed before publication.'))
            return redirect('testimonials_list')
    else:
        form = TestimonialForm()
    
    return render(request, 'testimonials/add_testimonial.html', {'form': form})