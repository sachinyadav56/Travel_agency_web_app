from django.contrib import admin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'seats_booked', 'total_price', 'paid', 'booking_date')
    list_filter = ('booking_date', 'tour', 'paid')
    search_fields = ('user__username', 'tour__title')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    readonly_fields = ('booking_date',)
    
    def total_price(self, obj):
        return obj.seats_booked * obj.tour.price
    total_price.short_description = "Total Price (₹)"