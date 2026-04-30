from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from .forms import (
    Generation,
    NameScheduleForm,
    DateTimeScheduleForm,
    ActionScheduleForm,
    TextActionForm,
    RulesScheduleForm,
    Scheduler
)
from .models import ProblemName


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


def automatic_creation(request, pk=None):
    template_name = 'generation/automatic.html'
    category = ProblemName.objects.using('postgres_zbx')\
    .values('problem_name')\
    .distinct()\
    .order_by('problem_name')

    type_data = [list(row.values()) for row in category]
    column_category = ['problem_name']

    # Получаем объект Scheduler, если передан pk
    scheduler_instance = None
    name_instance = None
    date_instance = None
    action_instance = None
    text_instance = None

    if pk is not None:
        scheduler_instance = get_object_or_404(Scheduler, pk=pk)
        # Получаем связанные объекты
        name_instance = scheduler_instance.description_schedule
        date_instance = scheduler_instance.date_time_schedule
        action_instance = scheduler_instance.action_schedule
        text_instance = scheduler_instance.text_action

    # Передаем правильные instance в формы
    name_form = NameScheduleForm(
        request.POST or None, instance=name_instance) # Имя правила
    date_form = DateTimeScheduleForm(
        request.POST or None, instance=date_instance) # Периодичность запуска
    action_form = ActionScheduleForm( 
        request.POST or None, instance=action_instance) # Настройка правила Тип оповещения о событии
    text_action_form = TextActionForm(
        request.POST or None, instance=text_instance) # Настройка правила текст оповещения


    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids') 
        if not selected_ids:
            messages.error(request, "❌ Вы не выбрали ни одной категории!")
        else:
            if (name_form.is_valid() and
                date_form.is_valid() and
                action_form.is_valid() and
                text_action_form.is_valid()):
                try:
                    name_instance = name_form.save()
                    date_instance = date_form.save()
                    text_action_instance = text_action_form.save()
                    action_id = request.POST.get('action_name')

                    if scheduler_instance:
                        # Редактирование существующего расписания
                        scheduler_instance.user_create_schedule = request.user.username
                        scheduler_instance.description_schedule_id = name_instance.id
                        scheduler_instance.date_time_schedule_id = date_instance.id
                        scheduler_instance.action_schedule_id = action_id
                        scheduler_instance.text_action_id = text_action_instance.id
                        scheduler_instance.save()
                        messages.success(
                            request, "✅ Расписание успешно обновлено!")
                    else:
                        # Создание нового расписания
                        Scheduler.objects.create(
                            user_create_schedule=request.user.username,
                            description_schedule_id=name_instance.id,
                            date_time_schedule_id=date_instance.id,
                            action_schedule_id=action_id,
                            text_action_id=text_action_instance.id
                        )
                        messages.success(
                            request, "✅ Расписание успешно создано!")
                        # Очищаем формы только при создании
                        name_form = NameScheduleForm()
                        date_form = DateTimeScheduleForm()
                        action_form = ActionScheduleForm()
                        text_action_form = TextActionForm()

                except Exception as e:
                    messages.error(
                        request, f"❌ Ошибка при сохранении данных: {e}")

    shedule = Scheduler.objects.all()
    field_names = [field.name for field in Scheduler._meta.get_fields()]

    context = {
        'name_form': name_form,
        'date_form': date_form,
        'action_form': action_form,
        'text_action_form': text_action_form,
        'type': type_data,
        'column_category': column_category,
        'shedule_list': shedule,
        'shedule_fields_name': field_names,
    }
    return render(request, template_name, context)
