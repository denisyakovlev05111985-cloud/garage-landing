from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time

from .models import Booking, Review, Service


# Генерация слотов: 09:00, 09:30, ..., 18:30 (без 19:30)
TIME_SLOTS = []
for h in range(9, 20):
    for m in (0, 30):
        if h == 19 and m == 30:
            continue
        TIME_SLOTS.append((f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}"))


class BookingForm(forms.ModelForm):
    date = forms.DateField(
        label='Дата записи',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
    )
    time_slot = forms.ChoiceField(
        label='Время записи',
        choices=TIME_SLOTS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Booking
<<<<<<< Updated upstream
        # ВАЖНО: сюда добавляем только те поля, которые реально есть в модели Booking
=======
>>>>>>> Stashed changes
        fields = ['name', 'phone', 'service']
        labels = {
            'name': 'Ваше имя',
            'phone': 'Телефон',
            'service': 'Услуга',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7XXXXXXXXXX'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['service'].empty_label = '— выберите услугу —'

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < timezone.localdate():
            raise ValidationError('Нельзя выбрать прошедшую дату.')
        return d

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) == 11 and digits[0] in ('7', '8'):
            digits = '7' + digits[1:]
        elif len(digits) == 10:
            digits = '7' + digits
        if len(digits) != 11:
            raise ValidationError('Введите телефон в формате +7XXXXXXXXXX')
        return '+' + digits

    def clean(self):
        cleaned_data = super().clean()
<<<<<<< Updated upstream
        date_val = cleaned_data.get('date')
        time_str = cleaned_data.get('time_slot')

        # Если одно из полей невалидно, дальше не проверяем
        if not date_val or not time_str:
=======
        d = cleaned_data.get('date')
        t = cleaned_data.get('time_slot')
        if not d or not t:
>>>>>>> Stashed changes
            return cleaned_data

        h, m = map(int, t.split(':'))
        naive = datetime.combine(d, time(h, m))
        # Делаем aware в текущей TZ (Europe/Moscow)
        aware = timezone.make_aware(naive, timezone.get_current_timezone())

<<<<<<< Updated upstream
        # Проверка на дубликат: ищем уже существующую запись на это точное время
        existing_bookings = Booking.objects.filter(date_time=combined_dt)
        if existing_bookings.exists():
            self.add_error('time_slot', 'Это время уже занято. Пожалуйста, выберите другой слот.')

        # Сохраняем собранное datetime во временный атрибут, чтобы потом использовать в save()
        self.cleaned_datetime = combined_dt
=======
        if aware < timezone.now():
            self.add_error('time_slot', 'Это время уже прошло.')
        elif Booking.objects.filter(date_time=aware).exists():
            self.add_error('time_slot', 'Это время уже занято. Выберите другой слот.')

        self.cleaned_datetime = aware
>>>>>>> Stashed changes
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_time = getattr(self, 'cleaned_datetime', None)
        if commit:
            instance.save()
        return instance


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите, что понравилось в работе шиномонтажа...',
                'class': 'form-control',
            }),
        }