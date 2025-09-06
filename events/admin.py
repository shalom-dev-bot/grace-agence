from django.contrib import admin
from .models import EventType, InvitationCard, Event, EventService

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(InvitationCard)
class InvitationCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'style', 'is_active', 'created_at')
    list_filter = ('style', 'is_active')
    search_fields = ('name',)

class EventServiceInline(admin.TabularInline):
    model = EventService
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'event_type', 'event_date', 'status', 'created_at')
    list_filter = ('status', 'event_type', 'event_date')
    search_fields = ('title', 'user__email', 'user__username')
    inlines = [EventServiceInline]
    date_hierarchy = 'event_date'
    fields = ('user', 'title', 'description', 'event_type', 'event_date', 'location', 'guest_count', 'budget', 'invitation_card', 'status', 'image')  # Ajout du champ image