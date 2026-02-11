
from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from bookings.models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        # Here you can integrate real payment API
        booking.paid = True
        booking.save()
        messages.success(request, "Payment successful! 🎉")
        return redirect('my_bookings')  # redirect to bookings page

    return render(request, 'payment_page.html', {'booking': booking})


