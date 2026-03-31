from django.http import HttpResponse

def monitoring_detail(request,pk):    
    return HttpResponse(f'Cтраница мониторинга {pk}')

def monitoring(request):    
    return HttpResponse(f'Cтраница мониторинга ')
