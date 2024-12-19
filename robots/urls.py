from django.urls import path
from .views import create_robot
from .views import download_excel_summary
from .views import order_robot
from . import views

urlpatterns = [
    path('create/', create_robot, name='create_robot'),
    path('download-summary/', download_excel_summary, name='download_excel_summary'),
    path('order/', order_robot, name='order_robot'),
    path('order/<str:model>/<str:version>/', views.order_robot, name='order_robot'),
    path('update_quantity/<str:model>/<str:version>/<int:quantity>/', views.update_robot_quantity, name='update_robot_quantity'),
]
