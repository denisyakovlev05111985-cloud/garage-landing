from django.db import models
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?7?\d{10}$',
    message='Телефон в формате +7XXXXXXXXXX или 10 цифр'
)


class Service(models.Model):
    name = models.CharField("Название услуги", max_length=200, unique=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    description = models.TextField("Описание", blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name} — {self.price} ₽"


class Booking(models.Model):
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20, validators=[phone_validator])
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Услуга",
    )
    # unique=True — защита от двойной записи на один слот
    date_time = models.DateTimeField("Дата и время записи", unique=True)
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    class Meta:
        ordering = ['date_time']
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return f"{self.name} — {self.date_time:%d.%m.%Y %H:%M}"


class WorkExample(models.Model):
    image = models.ImageField("Фото работы", upload_to="work_examples/", blank=True, null=True)
    image_url = models.URLField("Ссылка на фото", blank=True)
    caption = models.CharField("Подпись", max_length=250)

    class Meta:
        verbose_name = "Пример работы"
        verbose_name_plural = "Примеры работ"

    def __str__(self):
        return self.caption


class Review(models.Model):
    name = models.CharField("Имя клиента", max_length=100)
    text = models.TextField("Отзыв")
    is_published = models.BooleanField("Опубликован", default=False)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.name}"


class ContactInfo(models.Model):
    address = models.CharField("Адрес", max_length=255)
    phone = models.CharField("Телефон", max_length=50)
    email = models.EmailField("Email", blank=True, null=True)
    working_hours = models.CharField("Часы работы", max_length=100)

    map_latitude = models.DecimalField("Широта", max_digits=9, decimal_places=6, null=True, blank=True)
    map_longitude = models.DecimalField("Долгота", max_digits=9, decimal_places=6, null=True, blank=True)
    zoom = models.PositiveSmallIntegerField("Масштаб (зум)", default=17)

    # Храним ТОЛЬКО ссылку, iframe собираем в шаблоне
    map_url = models.URLField(
        "Ссылка на карту",
        blank=True,
        help_text="Например: https://yandex.ru/map-widget/v1/?um=constructor%3A...&source=constructor"
    )

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def save(self, *args, **kwargs):
        # Ровно одна запись в таблице
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.address