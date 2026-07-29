from django.db import models

class Booking(models.Model):
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    service = models.CharField("Услуга", max_length=50)
    date_time = models.DateTimeField("Дата и время записи")  
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.service} в {self.date_time}"
    
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
    address = models.CharField("Адрес", max_length=255)
    phone = models.CharField("Телефон", max_length=50)
    email = models.EmailField("Email", blank=True, null=True)
    working_hours = models.CharField("Часы работы", max_length=100)

    map_latitude = models.DecimalField(
        "Широта", max_digits=9, decimal_places=6, null=True, blank=True
    )
    map_longitude = models.DecimalField(
        "Долгота", max_digits=9, decimal_places=6, null=True, blank=True
    )
    zoom = models.PositiveSmallIntegerField("Масштаб (зум)", default=17)

    map_iframe_url = models.TextField(
        "HTML iframe карты",
        blank=True,
        null=True,
        help_text=(
            '<iframe src="https://yandex.ru/map-widget/v1/'
            '?um=constructor%3A221a76d2fd650a12d87390ffd2acf934652d7d8d2c487967f8dd1001a3fe1dff&amp;source=constructor" '
            'width="100%" frameborder="0" style="border:none;" allowfullscreen=""></iframe>'
        ),
    )

    def __str__(self):
        return self.address
