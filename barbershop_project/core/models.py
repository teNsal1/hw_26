from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Модель для хранения информации о мастерах
class Master(models.Model):
    # Основные поля модели
    name = models.CharField(max_length=150, verbose_name="Имя")  # Полное имя мастера
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")  # Фото профиля
    phone = models.CharField(max_length=20, verbose_name="Телефон")  # Контактный телефон
    address = models.CharField(max_length=255, verbose_name="Адрес")  # Адрес работы
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")  # Стаж в годах
    is_active = models.BooleanField(default=True, verbose_name="Активен")  # Флаг активности мастера

    def __str__(self):
        return self.name  # Строковое представление объекта

    class Meta:
        verbose_name = "Мастер"  # Название модели в единственном числе
        verbose_name_plural = "Мастера"  # Название модели во множественном числе


# Модель для хранения информации об услугах
class Service(models.Model):
    # Основные характеристики услуги
    name = models.CharField(max_length=200, verbose_name="Название")  # Наименование услуги
    masters = models.ManyToManyField(Master, related_name='services_offered')
    description = models.TextField(blank=True, verbose_name="Описание")  # Детальное описание
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")  # Стоимость услуги
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах")  # Длительность в минутах
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")  # Признак популярной услуги
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")  # Иллюстрация услуги

    def __str__(self):
        return self.name  # Строковое представление объекта

    class Meta:
        verbose_name = "Услуга"  # Название модели в единственном числе
        verbose_name_plural = "Услуги"  # Название модели во множественном числе


# Модель для управления заказами
class Order(models.Model):
    # Варианты статусов заказа
    STATUS_CHOICES = [
        ('not_approved', 'Не подтвержден'),
        ('approved', 'Подтвержден'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    # Поля заказа
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")  # Имя заказчика
    phone = models.CharField(max_length=20, verbose_name="Телефон")  # Контактный телефон клиента
    comment = models.TextField(blank=True, verbose_name="Комментарий")  # Дополнительные пожелания
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="not_approved", 
        verbose_name="Статус"
    )  # Текущий статус заказа
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Дата создания записи
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")  # Дата последнего изменения
    master = models.ForeignKey(
        Master, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Мастер"
    )  # Связанный мастер (может быть не назначен)
    services = models.ManyToManyField(
        Service, 
        related_name="orders", 
        verbose_name="Услуги"
    )  # Выбранные услуги (связь многие-ко-многим)
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")  # Запланированное время визита

    def __str__(self):
        return f"Заказ #{self.id} - {self.client_name}"  # Строковое представление объекта

    class Meta:
        verbose_name = "Заказ"  # Название модели в единственном числе
        verbose_name_plural = "Заказы"  # Название модели во множественном числе
        ordering = ['-date_created']  # Сортировка по умолчанию (новые записи сверху)


# Модель для хранения отзывов о мастерах
class Review(models.Model):
    # Варианты оценок
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    # Поля отзыва
    text = models.TextField(verbose_name="Текст отзыва")  # Содержание отзыва
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")  # Имя автора (опционально)
    master = models.ForeignKey(
        Master, 
        on_delete=models.CASCADE, 
        verbose_name="Мастер"
    )  # Связанный мастер
    photo = models.ImageField(
        upload_to="reviews/", 
        blank=True, 
        null=True, 
        verbose_name="Фотография"
    )  # Дополнительное фото (опционально)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Дата создания отзыва
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )  # Оценка от 1 до 5
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")  # Флаг публикации

    def __str__(self):
        return f"Отзыв от {self.client_name}"  # Строковое представление объекта

    class Meta:
        verbose_name = "Отзыв"  # Название модели в единственном числе
        verbose_name_plural = "Отзывы"  # Название модели во множественном числе
        ordering = ['-created_at']  # Сортировка по дате (новые сверху)