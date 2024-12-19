from django.db import models


SUPPORTED_MODELS = ["R2", "13", "X5"]

class Robot(models.Model):
    """
    Модель для представления данных о роботах, произведённых на заводе.
    """
    model = models.CharField(
        max_length=2,
        help_text="Двухсимвольная модель робота, например 'R2'",
        verbose_name="Модель"
    )
    version = models.CharField(
        max_length=10,
        help_text="Версия модели, например 'D2'",
        verbose_name="Версия"
    )
    created_at = models.DateTimeField(
        help_text="Дата и время производства робота",
        verbose_name="Дата производства"
    )

    def __str__(self):
        return f"{self.model}-{self.version}"

    class Meta:
        verbose_name = "Робот"
        verbose_name_plural = "Роботы"
        ordering = ['-created_at']



class Order(models.Model):
    model = models.CharField(max_length=50)  # Модель робота
    version = models.CharField(max_length=50)  # Версия робота
    customer_email = models.EmailField()  # Электронная почта клиента
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания заказа
    fulfilled = models.BooleanField(default=False)  # Статус выполнения заказа

    def __str__(self):
        return f"{self.model} {self.version} - {self.customer_email}"

