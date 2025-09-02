from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EventType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class InvitationCard(models.Model):
    CARD_STYLES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('vip', 'VIP'),
    ]
    
    name = models.CharField(max_length=100)
    style = models.CharField(max_length=20, choices=CARD_STYLES)
    template_content = models.TextField()
    preview_image = models.ImageField(upload_to='card_previews/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_style_display()})"

class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('planning', 'Planning'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True)
    guest_count = models.PositiveIntegerField(default=0)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invitation_card = models.ForeignKey(InvitationCard, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.email}"

class EventService(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_services')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'service']

    def __str__(self):
        return f"{self.event.title} - {self.service.name}"