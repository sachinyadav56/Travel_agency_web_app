from django.db import models


class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')

    def __str__(self):
        return self.name


class TourPackage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='tours'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TourImage(models.Model):
    tour = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='tours/gallery/')

    def __str__(self):
        return f"{self.tour.title} Image"
