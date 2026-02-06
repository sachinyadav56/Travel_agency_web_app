from django.urls import path
from bookings import views

urlpatterns = [
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]

