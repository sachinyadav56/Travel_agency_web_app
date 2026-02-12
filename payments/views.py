from django.shortcuts import redirect, render, get_object_or_404
from bookings.models import Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
import base64


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

    # ✅ Calculate total amount
    total_amount = booking.tour.price * booking.seats_booked

    if request.method == "POST":
        payment_method = request.POST.get('method')
        
        if payment_method == 'upi':
            # Generate UPI QR Code
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
            # Pay Later (On Arrival) - Just save payment method
            booking.payment_method = "arrival"  # ✅ Use 'arrival' to match your model
            booking.paid = False
            booking.save()
            
            # ✅ Show message on my_bookings page after redirect
            messages.success(request, "✅ Booking confirmed! Payment will be collected on arrival.")
            return redirect('my_bookings')

    # ✅ Pass total_amount to template
    return render(request, 'payment_page.html', {
        'booking': booking,
        'total_amount': total_amount
    })


@login_required
def payment_success(request, booking_id):
    """Called after successful UPI payment"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    booking.paid = True
    booking.payment_method = "online"  # ✅ Use 'online' to match your model
    booking.save()
    
    messages.success(request, "✅ Payment successful! Your booking is confirmed.")
    return redirect('my_bookings')


@login_required
def payment_failed(request, booking_id):
    """Called if UPI payment fails"""
    messages.error(request, "❌ Payment failed. Please try again.")
    return redirect('payment_page', booking_id=booking_id)