from django.contrib import admin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .models import Booking

Booking.objects.count()

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'tour',
        'seats_booked',
        'total_price',
        'booking_date'
    )

    list_filter = ('booking_date', 'tour')
    search_fields = ('user__username', 'tour__title')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    readonly_fields = ('booking_date',)
    list_per_page = 10

    # ✅ Total price per booking
    def total_price(self, obj):
        return obj.seats_booked * obj.tour.price
    total_price.short_description = "Total Price (₹)"

    # ✅ Show total revenue in changelist
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            queryset = response.context_data['cl'].queryset

            total_revenue = queryset.aggregate(
                revenue=Sum(
                    ExpressionWrapper(
                        F('seats_booked') * F('tour__price'),
                        output_field=DecimalField()
                    )
                )
            )['revenue'] or 0

            response.context_data['total_revenue'] = total_revenue

        except (AttributeError, KeyError):
            pass

        return response
