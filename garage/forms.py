from django import forms

class BookingForm(forms.Form):
    SERVICE_CHOICES = [
        ('shino', 'Шиномонтаж'),
        ('balance', 'Балансировка'),
        ('repair', 'Ремонт прокола'),
        ('disk_repair', 'Правка диска'),
        ('other', 'Другое'),
    ]

    name = forms.CharField(label="Ваше имя", max_length=100, widget=forms.TextInput(attrs={"placeholder": "Иван Иванов"}))
    phone = forms.CharField(label="Телефон", max_length=20, widget=forms.TextInput(attrs={"placeholder": "+7 (999) 000-00-00"}))
    service = forms.ChoiceField(label="Услуга", choices=SERVICE_CHOICES)
    time = forms.TimeField(label="Удобное время", widget=forms.TimeInput(attrs={"type": "time"}))
