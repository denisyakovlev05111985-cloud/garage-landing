from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, WorkExample, ContactInfo, Booking
from .forms import BookingForm

def index(request):
    services = Service.objects.all()
    examples = WorkExample.objects.all()[:6]
    contact = ContactInfo.objects.first()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()  # <-- это вызовет твой метод save() в форме, где собирается date_time
            messages.success(request, "Ваша заявка успешно отправлена! Мы перезвоним вам в ближайшее время.")
            return redirect('index')
    else:
        form = BookingForm()

    return render(request, "garage/index.html", {
        "services": services,
        "examples": examples,
        "contact": contact,
        "form": form,
    })
