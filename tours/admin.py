from django.contrib import admin
from .models import Destination, TourPackage, TourImage


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


# ================= TOUR IMAGE INLINE =================
class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 3
    readonly_fields = ()
    show_change_link = True


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'available_seats')
    list_filter = ('destination',)
    search_fields = ('title', 'destination__name')
    list_editable = ('price', 'available_seats')
    ordering = ('destination',)
    inlines = [TourImageInline]





