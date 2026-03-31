from django.shortcuts import render

def index(request):
    template_name = 'homepage/index.html'
    title = 'Главная страница'
    promo_product = 'Iron carrot'
    lists = [
        'title1',
        'title2',
        'title3',
        'title4',
        'title5',
        'title6',
    ]
    context ={
        'lists': lists,
        'title': title,
    }
    return render(request, template_name, context)
