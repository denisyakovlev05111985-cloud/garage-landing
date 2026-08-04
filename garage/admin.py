from django.contrib import admin
from .models import Service, WorkExample, ContactInfo, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(WorkExample)
class WorkExampleAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image_or_url')

    def image_or_url(self, obj):
        if obj.image:
            return obj.image.name
        return obj.image_url or "—"
    image_or_url.short_description = "Фото"

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'working_hours')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'date_time', 'created_at')
    list_filter = ('service', 'date_time')
    search_fields = ('name', 'phone')
