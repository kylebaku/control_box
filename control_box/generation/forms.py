from django import forms
from core.const import (
    PRIORITY_CHOICES,
    ENVIRONMENT,
    TYPE_TT,
    COORDINATOR_ROLE
)
from core.query_psql import get_city_choices, get_role_choices
from .models import (
    Scheduler,
    RulesSchedule,
    ActionSchedule,
    TextAction,
    DateTimeSchedule,
    NameSchedule
)
from core.const import DAYS_OF_WEEK, TASK, MONTH


class TaskForm(forms.Form):
    task = forms.MultipleChoiceField(
        choices=TASK,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control', 'size': 3}),
        label='Периодичность выполнения',
        required=False
    )


class Generation(forms.Form):
    urls = forms.ChoiceField(
        choices=ENVIRONMENT,
        widget=forms.RadioSelect,
        label="Среда запроса",
        initial='test',
    )
    type_tt = forms.ChoiceField(
        choices=TYPE_TT,
        widget=forms.RadioSelect,
        label="Тип запроса",
        initial='Service',
    )
    priority = forms.ChoiceField(
        label="Приоритет",
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect,
        initial=4,
    )

    city = forms.ChoiceField(
        label='Город',
        choices=get_city_choices(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    executor = forms.ChoiceField(
        label='Роль ответственного',
        choices=get_role_choices(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    coordinator = forms.ChoiceField(
        choices=COORDINATOR_ROLE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=4,
    )
    sample_text = forms.CharField(
        label='Краткое описание',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    short_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Опишите проблему...'
        }),
        label="Детальное описание"
    )

    def __init__(self, *args, **kwargs):
        # Динамически изменять initial значение поля priority в зависимости от
        # выбранного type_tt. Это делается в __init__ методе формы,
        # получая данные из request.POST
        super().__init__(*args, **kwargs)

        if self.data.get('type_tt') == 'Service':
            self.fields['priority'].initial = 5

###############################################################################
# automatic form
###############################################################################


class SchedulerForm(forms.ModelForm):
    class Meta:
        model = Scheduler
        fields = '__all__'


class DateTimeScheduleForm(forms.ModelForm):
    monthly_schedule = forms.MultipleChoiceField(
        choices=MONTH,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 1,  # Количество видимых пунктов (можно настроить)
            'style': 'width: 100%;'
        }),
        label='',
        required=False
    )
    weekly_schedule = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 1,  # Количество видимых пунктов (можно настроить)
            'style': 'width: 100%;'
        }),
        label='',
        required=False
    )

    class Meta:
        model = DateTimeSchedule
        fields = '__all__'
        widgets = {
            'monts_shedule': forms.DateInput(
                attrs={'type': 'month', 'class': 'form-control'}),
            'week_schedule': forms.TextInput(
                attrs={'type': 'week', 'class': 'form-control'}),
            'time_schedule': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}),
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'})
        }


class NameScheduleForm(forms.ModelForm):
    class Meta:
        model = NameSchedule
        fields = '__all__'
        widgets = {
            'name_schedule': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задачи'
            }),
            'description_schedule': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 9,
                'placeholder': 'Введите описание задачи'
            }),
        }


class TextActionForm(forms.ModelForm):
    class Meta:
        model = TextAction
        fields = '__all__'


class ActionScheduleForm(forms.ModelForm):
    class Meta:
        model = ActionSchedule
        fields = '__all__'
        widgets = {
            'action_name': forms.DateInput(
                attrs={'class': 'form-control'}),
        }


class RulesScheduleForm(forms.ModelForm):
    class Meta:
        model = RulesSchedule
        fields = '__all__'


class ScrolingSQLForm(forms.Form):
    sql_query_count = forms.IntegerField(
        label='укажите количество срабатываний',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите число',
            'step': '1'
        })
    )
