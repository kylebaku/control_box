from django import forms
from core.const import PRIORITY_CHOICES, ENVIRONMENT 

class Generation(forms.Form):
    urls = forms.ChoiceField(
        choices=ENVIRONMENT,
        widget=forms.RadioSelect(),
        label="Выберите, в какой среде формировать запрос",
        initial='test',
    )
    short_description = forms.CharField(
        max_length=40,
        label="Описание",
        )
    cordinator = forms.CharField(
        label='Кординатор',
    )
    executor = forms.CharField(
        label='Роль ответственного',
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect(),
        initial=4,
    )
    type_tt = forms.CheckboxInput()
    data_create = forms.DateField(
        label='Дата отложенного запроса',
        widget=forms.DateInput(attrs={'type': 'date'})
        )
