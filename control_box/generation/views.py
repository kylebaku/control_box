from django.shortcuts import render
from .forms import (
    Generation,
    NameScheduleForm,
    DateTimeScheduleForm,
    ActionScheduleForm,
    TextActionForm,
    ScrolingSQLForm,
)
from monitoring.models import *

def generation(request):
    template_name = 'generation/generation.html'
    category = {generation: 'test generation'}
    context = {
        'type': category,
    }
    return render(request, template_name, context)


def hand_creation(request):
    template_name = 'generation/hand.html'
    # # Обработка редактирования записи
    # if request.method == 'GET' and 'fix_id' in request.GET:
    #     fix_id = request.GET.get('fix_id')

    # Обработка удаления всех записей
    if request.method == 'GET' and 'clear_all' in request.GET:
        request.session['deferred_requests'] = []

    # Удаляем выборочно запись из списка сесии
    if request.method == 'GET' and 'delete_id' in request.GET:
        delete_id = request.GET.get('delete_id')
        deferred_requests = request.session.get('deferred_requests', [])
        # Удаляем запись с указанным ID
        deferred_requests = [
            req for req in deferred_requests if req['id'] != int(delete_id)]
        # Перенумеровываем ID оставшихся записей
        for index, req in enumerate(deferred_requests, 1):
            req['id'] = index
        request.session['deferred_requests'] = deferred_requests

    form = Generation(request.GET or None, initial={'urls': 'test'})

    if form.is_valid():
        # получаем список из сессии
        deferred_requests = request.session.get('deferred_requests', [])
        # Перенумеровываем ID оставшихся записей
        for index, req in enumerate(deferred_requests, 1):
            req['id'] = index
        new_request = {
            'id': len(deferred_requests) + 1,
            'urls': form.cleaned_data['urls'],
            'type_tt': form.cleaned_data['type_tt'],
            'city': form.cleaned_data['city'],
            'priority': form.cleaned_data['priority'],
            'executor': form.cleaned_data['executor'],
            'coordinator': form.cleaned_data['coordinator'],
            'sample_text': form.cleaned_data['sample_text'],
            'short_description': form.cleaned_data['short_description'],
        }
        deferred_requests.append(new_request)
        request.session['deferred_requests'] = deferred_requests

    context = {
        'form': form,
        'deferred_requests': request.session.get('deferred_requests', []),
    }
    return render(request, template_name, context)


def value_category(request):
    template_name = 'generation/automatic.html'
    count_sql = ScrolingSQLForm(request.POST or None)
    if count_sql.is_valid():
        # Получаем значение из формы
        count = count_sql.cleaned_data['sql_query_count']
    context = {
        'count_form': count,
    }
    return render(request, template_name, context)

def automatic_creation(request):
    template_name = 'generation/automatic.html'
    name_form = NameScheduleForm(request.POST or None)
    date_form = DateTimeScheduleForm(request.POST or None)
    action_Form = ActionScheduleForm(request.POST or None)
    text_action_form = TextActionForm(request.POST or None)
    category = CategoryStok.objects.using('postgres_zbx').all().values()
    type_data = [list(row.values()) for row in category]
    column_category = [field.db_column or field.name for field in CategoryStok._meta.fields]
    if name_form.is_valid() and date_form.is_valid():
        # Если форма заполнена сохранить в БД
        pass
    context = {
        'name_form': name_form,
        'date_form': date_form,
        'action_form': action_Form,
        'text_action_form': text_action_form,
        'type': type_data,
        'column_category': column_category,
    }
    return render(request, template_name, context)


"""def automatic_creation(request):
    template_name = 'generation/automatic.html'
    form = TaskForm(request.POST)
    context = {'form': form}
    if form.is_valid():
        selected = form.cleaned_data['task']
        if 'Ежедневный запуск' in selected:
            name_form = NameScheduleForm()
           # request.session['task_type'] = name_form
            context = {
                'form': name_form
            }
            if form.is_valid():
                date_form = DateTimeScheduleForm()
                context = {
                    'form': date_form
                }
    return render(request, template_name, context)
"""
