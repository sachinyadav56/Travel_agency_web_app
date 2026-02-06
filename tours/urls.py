from django.urls import path
from tours import views

urlpatterns = [
     path('', views.home, name='home'),

    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<int:id>/', views.tour_detail, name='tour_detail'),
]
