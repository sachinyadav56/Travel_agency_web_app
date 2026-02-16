from django.contrib import admin
from .models import Destination, TourPackage, TourImage


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name',)  # ✅ Removed 'country' - it doesn't exist
    search_fields = ('name',)


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'available_seats')
    list_filter = ('destination',)
    search_fields = ('title', 'destination__name')
    inlines = [TourImageInline]