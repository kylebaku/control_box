from django import forms
from core.const import PRIORITY_CHOICES, ENVIRONMENT, TYPE_TT


class Generation(forms.Form):
    urls = forms.ChoiceField(
        choices=ENVIRONMENT,
        widget=forms.RadioSelect,
        label="Выберите, в какой среде формировать запрос",
        initial='test',
    )
    type_tt = forms.ChoiceField(
        choices=TYPE_TT,
        widget=forms.RadioSelect,
        label="Тип запроса",
        initial='Service',
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect,
        initial=4,
    )
    executor = forms.CharField(
        label='Роль ответственного',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    coordinator = forms.CharField(
        label='Координатор',
        widget=forms.TextInput(attrs={'class': 'form-control'})
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
