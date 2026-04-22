from django.contrib import admin
from .models import (
    TextAction,
    ActionSchedule,
    )

admin.site.empty_value_display = 'Поле не заполнено'

models_to_register = [
    TextAction,
    ActionSchedule,
]

for model in models_to_register:
    admin.site.register(model)
