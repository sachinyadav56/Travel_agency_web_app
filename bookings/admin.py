# from django.contrib import admin
# from django.db.models import Sum, F, ExpressionWrapper, DecimalField
# from .models import Booking

# from travel_project.admin import custom_admin_site

# @admin.register(Booking, site=custom_admin_site)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('user', 'tour', 'seats_booked', 'total_price', 'paid', 'booking_date')
#     list_filter = ('booking_date', 'tour', 'paid')
#     search_fields = ('user__username', 'tour__title')
#     date_hierarchy = 'booking_date'
#     ordering = ('-booking_date',)
#     readonly_fields = ('booking_date',)
    
#     def total_price(self, obj):
#         return obj.seats_booked * obj.tour.price
#     total_price.short_description = "Total Price (₹)"

from django.contrib import admin
from travel_project.admin import custom_admin_site
from .models import Booking


@admin.register(Booking, site=custom_admin_site)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'seats_booked', 'paid', 'booking_date')
    list_filter = ('booking_date', 'tour', 'paid')
    search_fields = ('user__username', 'tour__title')
    ordering = ('-booking_date',)
