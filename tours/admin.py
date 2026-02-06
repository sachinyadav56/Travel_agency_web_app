from django.contrib import admin
from .models import Destination, TourPackage, TourImage

admin.site.register(Destination)



class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 6


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'available_seats')
    inlines = [TourImageInline]


