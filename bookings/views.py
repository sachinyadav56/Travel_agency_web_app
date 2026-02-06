from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from tours.models import TourPackage




@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(TourPackage, id=tour_id)

    if request.method == "POST":
        seats = int(request.POST['seats'])

        if seats <= 0:
            messages.error(request, "Invalid seat count")
            return redirect('book_tour', tour_id=tour.id)

        if seats > tour.available_seats:
            messages.error(request, "Not enough seats available")
            return redirect('book_tour', tour_id=tour.id)

        # Create booking
        Booking.objects.create(
            user=request.user,
            tour=tour,
            seats_booked=seats
        )

        # Reduce seats
        tour.available_seats -= seats
        tour.save()

        messages.success(request, "Booking successful")
        return redirect('my_bookings')

    return render(request, 'book_tour.html', {'tour': tour})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

