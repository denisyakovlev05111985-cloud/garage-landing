from django.db import models

class Service(models.Model):
    name = models.CharField("Название услуги", max_length=200)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return f"{self.name} — {self.price} ₽"

class WorkExample(models.Model):
    image_url = models.URLField("Ссылка на фото")
    caption = models.CharField("Подпись", max_length=250)

    def __str__(self):
        return self.caption

class ContactInfo(models.Model):
    phone = models.CharField("Телефон", max_length=50)
    email = models.EmailField("Email", blank=True)
    address = models.TextField("Адрес")
    working_hours = models.TextField("Режим работы")

    def __str__(self):
        return self.address
