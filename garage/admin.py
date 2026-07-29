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
    list_display = ('address', 'phone', 'zoom')
    fieldsets = (
        ("Контакты", {"fields": ("address", "phone", "email", "working_hours")}),
        ("Карта (координаты)", {"fields": ("map_latitude", "map_longitude", "zoom")}),
        ("Карта (готовый виджет)", {"fields": ("map_iframe_url",)}),
    )
