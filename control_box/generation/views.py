from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (
    Generation,
    NameScheduleForm,
    DateTimeScheduleForm,
    ActionScheduleForm,
    TextActionForm,
    Scheduler,
    RulesScheduleForm
)
from .models import ProblemNameAdm, ProblemNameSop, ProblemNamePrint, RulesSchedule


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


def get_problem_names_as_list(model):
    """Получить список тригеров из таблиц zabbix"""
    return [list(row.values()) for row in
            model.objects.using('postgres_zbx')
            .values('problem_name')
            .distinct()
            .order_by('problem_name')]


def automatic_creation(request, pk=None):

    template_name = 'generation/automatic.html'
    type_data_adm = get_problem_names_as_list(ProblemNameAdm)
    type_data_sop = get_problem_names_as_list(ProblemNameSop)
    type_data_print = get_problem_names_as_list(ProblemNamePrint)
    column_category = ['problem_name']

    # Получаем объект Scheduler, если передан pk
    scheduler_instance = None
    name_instance = None
    date_instance = None
    action_instance = None
    text_instance = None
    rules_instance = None

    if pk is not None:
        scheduler_instance = get_object_or_404(Scheduler, pk=pk)
        # Получаем связанные объекты
        name_instance = scheduler_instance.description_schedule
        date_instance = scheduler_instance.date_time_schedule
        action_instance = scheduler_instance.action_schedule
        text_instance = scheduler_instance.text_action
        rules_instance = scheduler_instance.rules_schedule
    
    # Передаем правильные instance в формы
    name_form = NameScheduleForm(
        request.POST or None, instance=name_instance
    )
    date_form = DateTimeScheduleForm(
        request.POST or None, instance=date_instance
    )
    action_form = ActionScheduleForm(
        request.POST or None,
        initial={'action_name': action_instance} if action_instance and pk else {}
    )
    text_action_form = TextActionForm(
        request.POST or None, instance=text_instance
    )
    rules_schedule_form = RulesScheduleForm(
        request.POST or None, instance=rules_instance
    )

    if request.method == 'POST':
        # Получаем триггер из любой вкладки
        name_rules = (
            request.POST.get('name_rules') or 
            request.POST.get('name_rules_sop') or 
            request.POST.get('name_rules_printer') or 
            ''
        )
        
        count_rules = request.POST.get('count_rules')
        count_month = request.POST.get('month_over_month')
        count_week = request.POST.get('week_over_week')
        count_day = request.POST.get('day_over_day')
        device_type = request.POST.get('device_type')
        print(device_type)
        if (
            name_form.is_valid() and
            date_form.is_valid() and
            action_form.is_valid() and
            text_action_form.is_valid() and
            rules_schedule_form.is_valid()
        ):
            try:
                # Сохраняем базовые формы
                name_instance = name_form.save()
                date_instance = date_form.save()
                text_action_instance = text_action_form.save()
                action_id = action_form.cleaned_data['action_name'].id

                if scheduler_instance:
                    # РЕДАКТИРОВАНИЕ: обновляем существующий RulesSchedule
                    rules_instance = scheduler_instance.rules_schedule
                    
                    if rules_instance:
                        # Обновляем существующий объект
                        rules_instance.name_rules = name_rules
                        rules_instance.count_rules = int(count_rules) if count_rules else 0
                        rules_instance.month_over_month = int(count_month) if count_month else 0
                        rules_instance.week_over_week = int(count_week) if count_week else 0
                        rules_instance.day_over_day = int(count_day) if count_day else 0
                        rules_instance.device_type = device_type
                        rules_instance.save()
                        print(f"Обновлен RulesSchedule id={rules_instance.id}")
                    else:
                        # Если почему-то нет связанного RulesSchedule, создаем новый
                        rules_instance = RulesSchedule.objects.create(
                            name_rules=name_rules,
                            count_rules=int(count_rules) if count_rules else 0,
                            month_over_month=int(count_month) if count_month else 0,
                            week_over_week=int(count_week) if count_week else 0,
                            day_over_day=int(count_day) if count_day else 0,
                            device_type=device_type
                        )
                        print(f"Создан новый RulesSchedule id={rules_instance.id}")
                    
                    # Обновляем Scheduler
                    scheduler_instance.user_create_schedule = request.user.username
                    scheduler_instance.description_schedule_id = name_instance.id
                    scheduler_instance.date_time_schedule_id = date_instance.id
                    scheduler_instance.action_schedule_id = action_id
                    scheduler_instance.text_action_id = text_action_instance.id
                    scheduler_instance.rules_schedule_id = rules_instance.id
                    scheduler_instance.save()
                    messages.success(request, "✅ Расписание успешно обновлено!")
                    
                else:
                    # СОЗДАНИЕ: создаем новый RulesSchedule
                    rules_instance = RulesSchedule.objects.create(
                        name_rules=name_rules,
                        count_rules=int(count_rules) if count_rules else 0,
                        month_over_month=int(count_month) if count_month else 0,
                        week_over_week=int(count_week) if count_week else 0,
                        day_over_day=int(count_day) if count_day else 0,
                        device_type=device_type
                    )
                    
                    # Создаем новый Scheduler
                    Scheduler.objects.create(
                        user_create_schedule=request.user.username,
                        description_schedule_id=name_instance.id,
                        date_time_schedule_id=date_instance.id,
                        action_schedule_id=action_id,
                        text_action_id=text_action_instance.id,
                        rules_schedule_id=rules_instance.id
                    )
                    messages.success(request, "✅ Расписание успешно создано!")
                    
                return redirect('generation:automatic_creation')
                
            except Exception as e:
                print(f"Ошибка: {e}")
                messages.error(request, f"❌ Ошибка при сохранении данных: {e}")
                return redirect('generation:automatic_creation')

    shedule = Scheduler.objects.all()
    field_names = [field.name for field in Scheduler._meta.get_fields()]

    context = {
        'name_form': name_form,
        'date_form': date_form,
        'action_form': action_form,
        'text_action_form': text_action_form,
        'type_trigger_adm': type_data_adm,
        'type_trigger_sop': type_data_sop,
        'type_trigger_print': type_data_print,
        'column_category': column_category,
        'shedule_list': shedule,
        'shedule_fields_name': field_names,
        'rules_schedule': rules_schedule_form,
    }

    return render(request, template_name, context)


def automatic_delete(request, pk):

    if request.method == 'POST':
        instance = get_object_or_404(Scheduler, pk=pk)
        instance.delete()
        print("Удалено!")
        return redirect('generation:automatic_creation')
    return redirect('generation:automatic_creation')
