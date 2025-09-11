from django.contrib import admin
from django.utils.translation import gettext_lazy as _  # Ajout de l'import pour les traductions
from django.utils import timezone  # Ajout pour utiliser timezone.now()
from .models import EventType, InvitationCard, Event, EventService, EventVideo, Contact  # Ajout de Contact

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

@admin.register(EventVideo)
class EventVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'uploaded_at', 'is_featured')
    list_filter = ('is_featured', 'uploaded_at')
    search_fields = ('title', 'description', 'event__title')
    date_hierarchy = 'uploaded_at'
    list_editable = ('is_featured',)  # Permet de modifier is_featured directement dans la liste

    def get_queryset(self, request):
        # Optimisation pour charger les événements liés
        qs = super().get_queryset(request)
        return qs.select_related('event')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for managing contact messages with dynamic filtering and actions."""
    list_display = ('name', 'email', 'subject', 'status', 'created_at', 'responded_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    list_editable = ('status',)  # Permet de changer le statut directement dans la liste
    actions = ['mark_as_responded', 'mark_as_closed']

    def mark_as_responded(self, request, queryset):
        """Mark selected contacts as responded and set the responded_at date."""
        updated_count = queryset.update(status='responded', responded_at=timezone.now())
        self.message_user(request, f"{updated_count} contact(s) marked as responded.")
    mark_as_responded.short_description = _("Mark as Responded")

    def mark_as_closed(self, request, queryset):
        """Mark selected contacts as closed."""
        updated_count = queryset.update(status='closed')
        self.message_user(request, f"{updated_count} contact(s) marked as closed.")
    mark_as_closed.short_description = _("Mark as Closed")

    def get_queryset(self, request):
        # Optimisation pour charger les utilisateurs et événements liés
        qs = super().get_queryset(request)
        return qs.select_related('user', 'event')