from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Sum, F, ExpressionWrapper, DecimalField


class TravelAdminSite(AdminSite):
    """Custom Admin Site with Dashboard Statistics"""
    site_header = "Travel Agency Admin"
    site_title = "Travel Agency"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        """Override index to calculate and display dashboard statistics"""
        extra_context = extra_context or {}
        
        # Import here to avoid circular imports
        from bookings.models import Booking
        
        # Calculate Total Revenue
        revenue_data = Booking.objects.aggregate(
            revenue=Sum(
                ExpressionWrapper(
                    F('seats_booked') * F('tour__price'),
                    output_field=DecimalField()
                )
            )
        )
        total_revenue = revenue_data['revenue'] or 0
        
        # Calculate Total Bookings
        total_bookings = Booking.objects.count()
        
        # Calculate Total Seats
        total_seats_data = Booking.objects.aggregate(
            seats=Sum('seats_booked')
        )
        total_seats = total_seats_data['seats'] or 0
        
        # Add to context
        extra_context['total_revenue'] = total_revenue
        extra_context['total_bookings'] = total_bookings
        extra_context['total_seats'] = total_seats
        
        return super().index(request, extra_context)


# Create instance
admin_site = TravelAdminSite(name='travel_admin')