from django.http import HttpResponse

from django.shortcuts import render
from .forms import Generation
from .utils import calculate

def generation(request):
    template_name = 'generation/generation.html'
    category = {generation: 'test generation'}
    context = {
        'type': category,
    }
    return render(request, template_name, context)


def hand_creation(request):
    template_name = 'generation/hand.html'
    form = Generation(initial={'urls': 'test'}, data=request.GET or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        day = calculate(
            form.cleaned_data['data_create']
        )
        context.update({'date_create': day})
    return render(request, template_name, context)

def automatic_creation(request):
    template_name = 'generation/automatic.html'
    category = {automatic_creation: 'test automatic_creation'}
    context = {
        'type': category,
    }
    return render(request, template_name, context)
