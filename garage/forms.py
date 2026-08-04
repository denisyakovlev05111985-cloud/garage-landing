from django import forms
from django.core.exceptions import ValidationError
from datetime import time, datetime, date
from .models import Booking, Review

TIME_SLOTS = []
for h in range(9, 20):
    for m in [0, 30]:
        if h == 19 and m == 30:
            continue
        TIME_SLOTS.append((f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}"))

class BookingForm(forms.ModelForm):
    # Эти поля НЕ из модели, они нужны только для ввода и валидации
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

        fields = ['name', 'phone', 'service']
        labels = {
            'name': 'Ваше имя',
            'phone': 'Телефон',
            'service': 'Услуга (впишите название)',
        }

    def clean_date(self):
        date_val = self.cleaned_data['date']
        if date_val < date.today():
            raise ValidationError('Нельзя выбрать прошедшую дату.')
        return date_val

    def clean(self):
        cleaned_data = super().clean()
        date_val = cleaned_data.get('date')
        time_str = cleaned_data.get('time_slot')

        if not date_val or not time_str:
            return cleaned_data

        h, m = map(int, time_str.split(':'))
        time_val = time(h, m)
        combined_dt = datetime.combine(date_val, time_val)

        existing_bookings = Booking.objects.filter(date_time=combined_dt)
        if existing_bookings.exists():
            self.add_error('time_slot', 'Это время уже занято. Пожалуйста, выберите другой слот.')

        self.cleaned_datetime = combined_dt
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Используем то, что мы заранее собрали в clean()
        instance.date_time = getattr(self, 'cleaned_datetime', None)
        if commit:
            instance.save()
        return instance


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите, что понравилось в работе шиномонтажа...'}),
        }
