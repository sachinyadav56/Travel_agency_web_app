from django.urls import path
from bookings import views

urlpatterns = [
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
     path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
      path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    

]

