from django.shortcuts import render, get_object_or_404
from .models import TourPackage


def home(request):
    return render(request, 'home.html')

# LIST page
def tour_list(request):
    tours = TourPackage.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})


# TOUR DETAIL PAGE
def tour_detail(request, id):
    tour = get_object_or_404(TourPackage, id=id)
    return render(request, 'tour_detail.html', {'tour': tour})
