import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot, SUPPORTED_MODELS
from django.http import HttpResponse
from .utils import generate_excel_summary
from django.shortcuts import render, redirect
from .forms import OrderForm
from django.shortcuts import render

from django.shortcuts import render
from .services import get_weekly_robot_data, generate_excel_report

from django.http import JsonResponse
from .services import create_order_if_not_available, notify_customers_when_robot_is_available


@csrf_exempt
def create_robot(request):
    """
    API-endpoint для создания записи о роботе.
    """
    if request.method == "POST":
        try:
            # Парсинг входных данных
            data = json.loads(request.body)

            # Проверка обязательных полей
            required_fields = ['model', 'version', 'created']
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "Поля model, version, created обязательны"}, status=400)

            # Проверка модели на соответствие SUPPORTED_MODELS
            if data['model'] not in SUPPORTED_MODELS:
                return JsonResponse({"error": "Модель не поддерживается"}, status=400)

            # Создание записи
            robot = Robot(
                model=data['model'],
                version=data['version'],
                created_at=data['created']
            )
            robot.save()

            return JsonResponse({"message": "Робот успешно создан", "id": robot.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Некорректный JSON"}, status=400)

    return JsonResponse({"error": "Метод не поддерживается"}, status=405)





def download_excel_summary(request):
    """
    API для скачивания Excel-файла со сводкой за последнюю неделю.
    """
    workbook = generate_excel_summary()

    # Сохраняем файл в HTTP-ответ
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="robots_summary.xlsx"'
    workbook.save(response)

    return response





# def order_robot(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()  # Сохраняем заказ в базе данных
#             return redirect('order_success')  # Перенаправляем на страницу успешного заказа
#     else:
#         form = OrderForm()

#     return render(request, 'robots/order_form.html', {'form': form})






def download_robot_report(request):
    """
    Представление для скачивания Excel-отчета с данными о произведенных роботах за последнюю неделю.
    """
    weekly_data = get_weekly_robot_data()
    return generate_excel_report(weekly_data)


def order_robot(request, model=None, version=None):
    """
    Представление для оформления заказа на робота.
    Если робот в наличии, сразу покупаем, если нет — добавляем в очередь.
    """
    email = request.POST.get('email')  # Получаем email клиента из POST запроса
    if not email:
        return JsonResponse({'message': 'Email не предоставлен'}, status=400)

    # Заказ робота
    order = create_order_if_not_available(email, model, version)

    if order is None:
        return JsonResponse({'message': f'Робот {model} {version} заказан и успешно отправлен!'})
    
    return JsonResponse({'message': f'Робот {model} {version} сейчас нет в наличии. Мы уведомим вас, когда он появится.'})

def update_robot_quantity(request, model, version, quantity):
    """
    Функция для обновления количества роботов в наличии.
    Когда робот появляется в наличии, уведомляем клиентов.
    """
    robot = Robot.objects.filter(model=model, version=version).first()
    
    if robot:
        robot.quantity += quantity
        robot.save()
        # Уведомляем клиентов, что робот появился в наличии
        notify_customers_when_robot_is_available(robot)
        return JsonResponse({'message': f'Количество роботов {model} {version} обновлено!'})
    
    return JsonResponse({'message': f'Робот {model} {version} не найден!'}, status=404)




# В представлении (views.py)
def order_form(request, model, version):
    return render(request, 'robots/order_form.html', {'model': model, 'version': version})

