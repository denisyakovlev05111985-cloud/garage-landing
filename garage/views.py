from django.shortcuts import render
from .models import Service, WorkExample, ContactInfo
from .forms import BookingForm

def index(request):
    services = Service.objects.all()
    examples = WorkExample.objects.all()[:6]
    contact = ContactInfo.objects.first()
    form = BookingForm()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Здесь можно сохранить заявку или отправить уведомление
            pass

    return render(request, "garage/index.html", {
        "services": services,
        "examples": examples,
        "contact": contact,
        "form": form,
    })
