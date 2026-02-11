from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
]
