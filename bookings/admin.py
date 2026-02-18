from django.contrib import admin
from travel_project.admin import custom_admin_site
from .models import Booking


@admin.register(Booking, site=custom_admin_site)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'seats_booked', 'paid', 'booking_date')
    list_filter = ('booking_date', 'tour', 'paid')
    search_fields = ('user__username', 'tour__title')
    ordering = ('-booking_date',)
