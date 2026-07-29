from django.contrib import admin
from .models import Service, WorkExample, ContactInfo, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(WorkExample)
class WorkExampleAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image_url')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'phone', 'service', 'date_time', 'created_at')
    list_filter = ('date_time', 'created_at')  
    search_fields = ('name', 'phone')
