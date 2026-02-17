from django.contrib import admin
from travel_project.admin import custom_admin_site
from .models import Destination, TourPackage


@admin.register(Destination, site=custom_admin_site)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TourPackage, site=custom_admin_site)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'available_seats')
    list_filter = ('destination',)
