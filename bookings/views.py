from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from tours.models import TourPackage

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(TourPackage, id=tour_id)

    if request.method == "POST":
        seats = int(request.POST.get("seats"))

        if seats > tour.available_seats:
            messages.error(request, "Not enough seats available!")
            return render(request, 'book_tour.html', {'tour': tour})

        # Create booking with seats_booked
        booking = Booking.objects.create(
            user=request.user,
            tour=tour,
            seats_booked=seats  
        )

        # Reduce available seats
        tour.available_seats -= seats
        tour.save()

        # Redirect to payment page 
        return redirect('payment_page', booking_id=booking.id)

    return render(request, 'book_tour.html', {'tour': tour})


@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    tour = booking.tour

    # return seats
    tour.available_seats += booking.seats_booked
    tour.save()

    booking.delete()

    # UPDATED MESSAGE TEXT
    messages.success(request, " Booking cancel successfully")
    return redirect('my_bookings')


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    tours = TourPackage.objects.all()

    if request.method == "POST":
        new_tour_id = request.POST.get('tour')
        new_seats = int(request.POST.get('seats'))

        new_tour = get_object_or_404(TourPackage, id=new_tour_id)

        # restore old seats
        booking.tour.available_seats += booking.seats_booked
        booking.tour.save()

        # check availability
        if new_seats > new_tour.available_seats:
            messages.error(request, "❌ Not enough seats available")
            return redirect('edit_booking', booking_id=booking.id)

        #  update booking
        booking.tour = new_tour
        booking.seats_booked = new_seats
        booking.save()

        # reduce new seats
        new_tour.available_seats -= new_seats
        new_tour.save()

        #  Show success message on my_bookings page
        messages.success(request, "✏️ Booking updated successfully")
        return redirect('my_bookings')

    return render(request, 'edit_booking.html', {
        'booking': booking,
        'tours': tours
    })
    
@login_required
def payment_success(request, booking_id):
    """Called after successful UPI payment"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    booking.paid = True
    booking.payment_method = "online"  
    booking.save()
    
    # UPDATED MESSAGE TEXT
    messages.success(request, "Booking successful")
    return redirect('my_bookings')