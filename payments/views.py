# from django.shortcuts import redirect, render, get_object_or_404
# from bookings.models import Booking
# from django.contrib import messages

# from django.contrib.auth.decorators import login_required


# @login_required
# def payment_page(request, booking_id):
#     booking = get_object_or_404(
#         Booking,
#         id=booking_id,
#         user=request.user
#     )

#     # ❌ Prevent double payment
#     if booking.paid:
#         messages.info(request, "This booking is already paid.")
#         return redirect('my_bookings')

#     if request.method == "POST":
#         # Simulate payment success
#         booking.paid = True
#         booking.payment_method = "online"   # ✅ important
#         booking.save()

#         messages.success(request, "Payment successful! ")
#         return redirect('my_bookings')

#     return render(request, 'payment_page.html', {'booking': booking})


from django.shortcuts import redirect, render, get_object_or_404
from bookings.models import Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
import base64
from django.urls import reverse


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
        payment_method = request.POST.get('method')
        
        if payment_method == 'upi':
            # Generate UPI QR Code
            total_amount = booking.tour.price * booking.seats_booked
            
            # UPI string format: upi://pay?pa=UPI_ID&pn=NAME&am=AMOUNT&tn=DESCRIPTION
            upi_string = f"upi://pay?pa=your_upi_id@bank&pn=TravelAgency&am={total_amount}&tn=BookingID{booking_id}"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(upi_string)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for embedding in HTML
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return render(request, 'payment_page.html', {
                'booking': booking,
                'qr_code': qr_code_base64,
                'total_amount': total_amount,
                'show_qr': True
            })
        
        elif payment_method == 'cod':
            # Pay Later (On Arrival)
            booking.paid = False
            booking.payment_method = "cod"
            booking.save()
            
            messages.success(request, "✅ Booking confirmed! Payment will be collected on arrival.")
            return redirect('my_bookings')

    return render(request, 'payment_page.html', {'booking': booking})


@login_required
def payment_success(request, booking_id):
    """Called after successful UPI payment"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    booking.paid = True
    booking.payment_method = "upi"
    booking.save()
    
    messages.success(request, "✅ Payment successful! Your booking is confirmed.")
    return redirect('my_bookings')


@login_required
def payment_failed(request, booking_id):
    """Called if UPI payment fails"""
    messages.error(request, "❌ Payment failed. Please try again.")
    return redirect('payment_page', booking_id=booking_id)