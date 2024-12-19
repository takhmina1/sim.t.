from datetime import timedelta
from django.utils import timezone
from .models import Robot
from django.db.models import Sum
import openpyxl
from io import BytesIO
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Robot, Order



def get_weekly_robot_data():
    """
    Получение данных о произведенных роботах за последнюю неделю.
    """
    one_week_ago = timezone.now() - timedelta(days=7)
    
    weekly_data = Robot.objects.filter(created_at__gte=one_week_ago) \
                               .values('model', 'version') \
                               .annotate(total_quantity=Sum('quantity')) \
                               .order_by('model', 'version')
    
    return weekly_data




def generate_excel_report(weekly_data):
    """
    Генерация Excel отчета по данным о роботах за последнюю неделю.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Сводка за неделю"

    # Заголовки для таблицы
    ws.append(['Модель', 'Версия', 'Количество за неделю'])

    # Заполнение данными
    for data in weekly_data:
        ws.append([data['model'], data['version'], data['total_quantity']])

    # Сохранение в память (вместо записи на диск)
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    # Возвращаем файл как HTTP-ответ
    response = HttpResponse(file_stream, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="robot_report.xlsx"'
    
    return response





def send_availability_notification(order):
    """
    Отправка уведомления клиенту, когда робот становится доступным.
    """
    subject = f"Робот {order.robot_model} {order.robot_version} теперь в наличии!"
    message = f"Добрый день!\n\nНедавно вы интересовались нашим роботом модели {order.robot_model}, версии {order.robot_version}. Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.customer_email])

def create_order_if_not_available(email, model, version):
    """
    Создает заказ, если робот недоступен.
    """
    robot = Robot.objects.filter(model=model, version=version).first()
    
    if robot and robot.quantity > 0:
        # Если робот в наличии, сразу уменьшаем количество
        robot.quantity -= 1
        robot.save()
        return None  # Робот был в наличии, заказ не нужен
    
    # Если робота нет в наличии, добавляем заказ в очередь
    order = Order.objects.create(
        customer_email=email,
        robot_model=model,
        robot_version=version,
        is_available=False
    )
    
    return order

def notify_customers_when_robot_is_available(robot):
    """
    Сигнал для уведомления клиентов, когда робот становится доступным.
    """
    if robot.quantity > 0:
        orders = Order.objects.filter(robot_model=robot.model, robot_version=robot.version, is_available=False)
        
        for order in orders:
            send_availability_notification(order)
            order.is_available = True
            order.save()


