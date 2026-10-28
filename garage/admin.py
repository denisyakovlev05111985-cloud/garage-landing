from django.contrib import admin
from .models import Service, Booking, Review, ContactInfo, WorkExample


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date_time', 'service', 'created_at')
    list_filter = ('date_time', 'service')
    search_fields = ('name', 'phone')
    date_hierarchy = 'date_time'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'is_published')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('name', 'text')
    actions = ['publish', 'unpublish']

    @admin.action(description='Опубликовать выбранные')
    def publish(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Снять с публикации')
    def unpublish(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Разрешаем добавить только если записи ещё нет
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WorkExample)
class WorkExampleAdmin(admin.ModelAdmin):
    list_display = ('caption',)