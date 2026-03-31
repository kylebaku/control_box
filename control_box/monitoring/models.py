from django.db import models
from core.models import TimeModel


class MonitoringDevice(TimeModel):
    # Информация по типам устройств взятых на мониторинг VDI,PC,Print
    name = models.CharField(max_length=50, unique=True)


class ModelDevice(TimeModel):
    # Модели устройств Notebook 655, HP6305
    model = models.TextField()
    note = models.CharField(max_length=60)


class LocationOffice(TimeModel):
    # Тип локаций Админ, СОП
    name = models.CharField(
        max_length=120,
        unique=True
    )


class LocationName(TimeModel):
    # Полный адрес локации
    region = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    street = models.CharField(max_length=60)
    house = models.IntegerField()
    room = models.IntegerField()
    note = models.CharField(max_length=100)
    type = models.ForeignKey(
        LocationOffice,
        on_delete=models.SET_NULL,
        null=True
    )


class TypeDevice(TimeModel):
    # Тип устройства Notebook, VDI fullClone, Printer
    name = models.TextField()
    device_type = models.ForeignKey(
        MonitoringDevice,
        on_delete=models.SET_NULL,
        null=True
    )
    location = models.ForeignKey(
        LocationName,
        on_delete=models.SET_NULL,
        null=True
    )
    models = models.ForeignKey(
        ModelDevice,
        on_delete=models.SET_NULL,
        null=True
    )
