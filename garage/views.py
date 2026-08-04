from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Service, WorkExample, ContactInfo, Booking, Review
from .forms import BookingForm, ReviewForm
from django.utils import timezone
import json

def index(request):
    services = Service.objects.all()
    examples = WorkExample.objects.all()[:6]
    contact = ContactInfo.objects.first()
    reviews = Review.objects.order_by('-created_at')[:10]

    now = timezone.now()
    bookings_list = Booking.objects.filter(date_time__gte=now).order_by('date_time')

    bookings_data = [
        {
            "name": b.name,
            "phone": b.phone,
            "service": b.service,
            "date_time": b.date_time.strftime('%d.%m.%Y %H:%M'),
            "created_at": b.created_at.strftime('%d.%m.%Y %H:%M'),
        }
        for b in bookings_list
    ]
    bookings_json = json.dumps(bookings_data)

    booked_slots = [
        dt.strftime('%Y-%m-%d %H:%M')
        for dt in bookings_list.values_list('date_time', flat=True)
    ]
    booked_slots_json = json.dumps(booked_slots)

    form = BookingForm()
    review_form = ReviewForm()

    if request.method == "POST":
        # Обычная отправка (если JS отключён или не сработал)
        if 'booking_submit' in request.POST:
            form = BookingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Ваша заявка успешно отправлена!")
                return redirect('index')
            else:
                messages.error(request, "Ошибка в форме бронирования. Проверьте поля.")
        elif 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, "Спасибо за отзыв!")
                return redirect('index')

    return render(request, "garage/index.html", {
        "services": services,
        "examples": examples,
        "contact": contact,
        "reviews": reviews,
        "form": form,
        "review_form": review_form,
        "booked_slots_json": booked_slots_json,
        "bookings_json": bookings_json,
    })


# НОВЫЙ VIEW: AJAX-обработка бронирования
from django.views.decorators.csrf import csrf_exempt  # мы передаём токен через форму, но для fetch иногда удобно так
from django.views.decorators.http import require_POST

@require_POST
def booking_ajax(request):
    form = BookingForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            "status": "success",
            "message": "Ваша заявка успешно отправлена!"
        })
    # Возвращаем ошибки формы в JSON
    return JsonResponse({
        "status": "error",
        "errors": form.errors.get_json_data()
    }, status=400)
