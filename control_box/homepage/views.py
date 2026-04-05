from django.shortcuts import get_object_or_404, render
from monitoring.models import *


def index(request):
    template_name = 'homepage/index.html'
    device_monitoring = DeviceModel.objects.select_related('location') .order_by('-created_at')
    context = {
        'device_monitoring': device_monitoring,
    }
    return render(request, template_name, context)

# поделючение к postgesql
# from django.db import connections

# def index(request):
#     template_name = 'homepage/index.html'
#     with connections['postgres'].cursor() as cursor:
#         cursor.execute('SELECT * FROM "Category_stok" cs ')
#         rows = cursor.fetchall()

#     # Получаем названия колонок
#     columns = [col[0] for col in cursor.description] if rows else []

#     context = {
#         'data': rows,
#         'columns': columns,
#     }
#     return render(request, template_name, context)
