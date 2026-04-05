from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from monitoring.models import *


def monitoring_detail(request, pk):
    template_name = 'monitoring/detail.html'
    device_monitoring = get_object_or_404(
        DeviceModel.objects.all().filter(
            created_at__gt='2026-04-01 21:59:27.176660'
        ).order_by('model'),
        pk=pk
    )
    context = {
        'device_monitoring': device_monitoring,
    }
    return render(request, template_name, context)


def monitoring(request):
    return HttpResponse(f'Cтраница мониторинга ')
