from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, WorkExample, ContactInfo, Booking, Review
from .forms import BookingForm, ReviewForm
from django.utils import timezone
import json

def index(request):
    services = Service.objects.all()
    examples = WorkExample.objects.all()[:6]
    contact = ContactInfo.objects.first()
    reviews = Review.objects.order_by('-created_at')[:10]

    # Самый безопасный способ: сразу в JSON, без лишних замен в JS
    booked_slots = [
        dt.strftime('%Y-%m-%d %H:%M')
        for dt in Booking.objects.values_list('date_time', flat=True)
    ]
    booked_slots_json = json.dumps(booked_slots)  # Это будет валидный JSON-массив

    form = BookingForm()
    review_form = ReviewForm()

    if request.method == "POST":
        if 'booking_submit' in request.POST:
            form = BookingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Ваша заявка успешно отправлена!")
                return redirect('index')
            else:
                messages.error(request, "Ошибка в форме бронирования.")
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
        "booked_slots_json": booked_slots_json,  # Передаём уже готовый JSON
    })
