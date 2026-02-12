from django.shortcuts import redirect, render, get_object_or_404
from bookings.models import Booking
from django.contrib import messages

from django.contrib.auth.decorators import login_required


@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    # ❌ Prevent double payment
    if booking.paid:
        messages.info(request, "This booking is already paid.")
        return redirect('my_bookings')

    if request.method == "POST":
        # Simulate payment success
        booking.paid = True
        booking.payment_method = "online"   # ✅ important
        booking.save()

        messages.success(request, "Payment successful! ")
        return redirect('my_bookings')

    return render(request, 'payment_page.html', {'booking': booking})
