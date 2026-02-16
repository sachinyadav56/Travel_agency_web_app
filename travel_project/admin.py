from django.contrib import admin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField


class CustomAdminSite(admin.AdminSite):
    """Custom Admin Site"""
    site_header = "🌍 Travel Agency Admin"
    site_title = "Travel Agency Dashboard"
    index_title = "📊 Dashboard Overview"

    def index(self, request, extra_context=None):
        """Dashboard with statistics"""
        extra_context = extra_context or {}
        
        try:
            from bookings.models import Booking
            from tours.models import TourPackage
            
            # Revenue
            revenue_data = Booking.objects.aggregate(
                revenue=Sum(
                    ExpressionWrapper(
                        F('seats_booked') * F('tour__price'),
                        output_field=DecimalField()
                    )
                )
            )
            
            # Bookings
            total_bookings = Booking.objects.count()
            paid_bookings = Booking.objects.filter(paid=True).count()
            
            # Seats
            seats_data = Booking.objects.aggregate(
                seats=Sum('seats_booked')
            )
            
            # Tours
            total_tours = TourPackage.objects.count()
            
            extra_context.update({
                'total_revenue': revenue_data['revenue'] or 0,
                'total_bookings': total_bookings,
                'paid_bookings': paid_bookings,
                'total_seats': seats_data['seats'] or 0,
                'total_tours': total_tours,
            })
        except Exception as e:
            print(f"Dashboard error: {e}")
        
        return super().index(request, extra_context)


# Replace default admin
admin.site = CustomAdminSite(name='admin')