from django.contrib import admin
from .models import Robot

@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    """
    Конфигурация панели администратора для модели Robot.
    """
    list_display = ('id', 'model', 'version', 'created_at')  # Отображаемые поля в списке объектов
    list_filter = ('model', 'version', 'created_at')  # Фильтры по полям
    search_fields = ('model', 'version')  # Поля для поиска
    ordering = ('-created_at',)  # Порядок сортировки (новейшие сначала)
    readonly_fields = ('created_at',)  # Поля, недоступные для редактирования
