from django.contrib import admin
from .models import (
    TypeOffice,
    LocationOffice,
    DeviceModel,
    DeviceMonitoring,
    DeviceType,
)

admin.site.empty_value_display = 'Поле не заполнено' 

models_to_register = [
    TypeOffice,
    DeviceMonitoring,
    DeviceType,
]

for model in models_to_register:
    admin.site.register(model)


class MonitoringAdmin(admin.ModelAdmin):
    list_display = ('model', 'note', 'device_type_ref',
                    'device_type', 'location')
    list_filter = ('model', 'device_type',)
    list_display_links = ('model',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'region',
        'branch',
        'city',
        'street',
        'house',
        'room',
        'note',
    )
    list_filter = (
        'region',
        'branch',
        )

admin.site.register(LocationOffice, LocationAdmin)
admin.site.register(DeviceModel, MonitoringAdmin)
