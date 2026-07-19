from django.contrib import admin
from .models import Service, WorkExample, ContactInfo

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)

@admin.register(WorkExample)
class WorkExampleAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image_url')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'address', 'working_hours')
