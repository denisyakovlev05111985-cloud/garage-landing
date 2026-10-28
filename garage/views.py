import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Service, WorkExample, ContactInfo, Booking, Review
from .forms import BookingForm, ReviewForm


def index(request):
    services = Service.objects.all()
    examples = WorkExample.objects.all()[:6]
    contact = ContactInfo.load()
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:10]

    now = timezone.now()
    bookings_list = Booking.objects.filter(date_time__gte=now).order_by('date_time')

    # БЕЗ персональных данных: только дата/время занятых слотов
    bookings_data = [
        {
            "date_time": timezone.localtime(b.date_time).strftime('%d.%m.%Y %H:%M'),
        }
        for b in bookings_list
    ]
    bookings_json = json.dumps(bookings_data, ensure_ascii=False)

    # Список занятых слотов для JS (если понадобится блокировать в форме)
    booked_slots = [
        timezone.localtime(dt).strftime('%Y-%m-%d %H:%M')
        for dt in bookings_list.values_list('date_time', flat=True)
    ]
    booked_slots_json = json.dumps(booked_slots)

    form = BookingForm()
    review_form = ReviewForm()

    if request.method == "POST":
        # Обычная отправка (если JS отключён)
        if 'booking_submit' in request.POST:
            form = BookingForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Ваша заявка успешно отправлена!")
                    return redirect('index')
                except IntegrityError:
                    form.add_error('time_slot', 'Это время только что заняли. Выберите другое.')
                    messages.error(request, "Это время только что заняли. Выберите другое.")
            else:
                messages.error(request, "Ошибка в форме бронирования. Проверьте поля.")

        elif 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, "Спасибо за отзыв! Он появится после модерации.")
                return redirect('index')
            else:
                messages.error(request, "Исправьте ошибки в форме отзыва.")

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


@require_POST
def booking_ajax(request):
    form = BookingForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({
                "status": "success",
                "message": "Ваша заявка успешно отправлена!"
            })
        except IntegrityError:
            return JsonResponse({
                "status": "error",
                "errors": {
                    "time_slot": [{"message": "Это время только что заняли. Выберите другое."}]
                }
            }, status=400)

    # Приводим ошибки к формату, который ждёт JS: {field: [{message: "..."}]}
    errors = {}
    for field, errs in form.errors.get_json_data().items():
        errors[field] = [{"message": e["message"]} for e in errs]

    return JsonResponse({
        "status": "error",
        "errors": errors
    }, status=400)