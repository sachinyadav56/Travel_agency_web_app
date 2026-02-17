from django.contrib import admin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField


class CustomAdminSite(admin.AdminSite):
    site_header = "🌍 Travel Agency Admin"
    site_title = "Travel Agency Dashboard"
    index_title = "📊 Dashboard Overview"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        try:
            from bookings.models import Booking
            from tours.models import TourPackage

            revenue_data = Booking.objects.aggregate(
                revenue=Sum(
                    ExpressionWrapper(
                        F('seats_booked') * F('tour__price'),
                        output_field=DecimalField()
                    )
                )
            )

            total_bookings = Booking.objects.count()
            total_seats = Booking.objects.aggregate(
                seats=Sum('seats_booked')
            )['seats'] or 0

            total_tours = TourPackage.objects.count()

            extra_context.update({
                'total_revenue': revenue_data['revenue'] or 0,
                'total_bookings': total_bookings,
                'total_seats': total_seats,
                'total_tours': total_tours,
            })

        except Exception as e:
            print("Dashboard error:", e)

        return super().index(request, extra_context)


custom_admin_site = CustomAdminSite(name='custom_admin')
