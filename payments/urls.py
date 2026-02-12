from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment/success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('payment/failed/<int:booking_id>/', views.payment_failed, name='payment_failed'),
]
