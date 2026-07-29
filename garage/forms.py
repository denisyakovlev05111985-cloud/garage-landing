from django import forms
from .models import Booking
from datetime import time, datetime

# Генерируем список слотов: каждые 30 минут с 09:00 до 19:00
TIME_SLOTS = []
for h in range(9, 20):
    for m in [0, 30]:
        if h == 19 and m == 30:
            continue
        # В choices: (значение для бэкенда, текст для отображения)
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
        fields = ['name', 'phone', 'service']
        labels = {
            'name': 'Ваше имя',
            'phone': 'Телефон',
            'service': 'Услуга',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        date_val = self.cleaned_data['date']
        time_str = self.cleaned_data['time_slot']  # это строка "ЧЧ:ММ"

        # Превращаем строку "14:30" в объект datetime.time
        h, m = map(int, time_str.split(':'))
        time_val = time(h, m)

        instance.date_time = datetime.combine(date_val, time_val)

        if commit:
            instance.save()
        return instance
