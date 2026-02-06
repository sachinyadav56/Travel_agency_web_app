from django.db import models
from django.contrib.auth.models import User
from tours.models import TourPackage

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    seats_booked = models.IntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"

