from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order, Robot

@receiver(post_save, sender=Robot)
def send_order_email_notification(sender, instance, created, **kwargs):
    """
    Сигнал, который отправляет email, когда робот становится доступен.
    """
    if created:  # Сигнал срабатывает, когда создается новый робот
        # Проверяем, есть ли заказ на эту модель и версию
        orders = Order.objects.filter(model=instance.model, version=instance.version, fulfilled=False)

        for order in orders:
            # Отправляем email уведомление
            send_mail(
                'Ваш заказ на робота в наличии!',
                f'Добрый день!\n\nНедавно вы интересовались нашим роботом модели {order.model}, версии {order.version}. Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.',
                'takhminaacom@gmail.com',  # От кого
                [order.customer_email],  # Кому
            )
            # Обновляем статус выполнения заказа
            order.fulfilled = True
            order.save()
