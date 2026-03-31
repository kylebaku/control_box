from django.http import HttpResponse

def report(request):    
    return HttpResponse(f'Отчеты')

def report_list(request,pk):    
    return HttpResponse(f'Отчеты {pk}') 