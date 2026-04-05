from django.db import models
from core.models import TimeModel


class DeviceMonitoring(TimeModel):
    # Информация по типам устройств взятых на мониторинг VDI,PC,Print
    name = models.CharField(
        max_length=50, unique=True,
        verbose_name='Типа устройства взятого на мониторинг'
        )

    class Meta:
        verbose_name = 'Тип устройства взятого на мониторинг'
        verbose_name_plural = 'Типы устройств взятых на мониторинг'

    def __str__(self):
        return self.name


class TypeOffice(TimeModel):
    # Тип локаций Админ, СОП
    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name='Тип локации'
    )

    class Meta:
        verbose_name = 'Тип офиса'
        verbose_name_plural = 'Типы офисов'

    def __str__(self):
        return self.name


class LocationOffice(TimeModel):
    # Полный адрес локации
    region = models.CharField(max_length=40, verbose_name='Регион')
    branch = models.CharField(max_length=40, verbose_name='Филиал')
    city = models.CharField(max_length=40, verbose_name='Город')
    street = models.CharField(max_length=60, verbose_name='Улица')
    house = models.IntegerField(verbose_name='Дом')
    room = models.IntegerField(verbose_name='Комната')
    note = models.CharField(max_length=100, verbose_name='Заметка', blank=True)
    type = models.ForeignKey(
        TypeOffice,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип локации'
    )

    class Meta:
        verbose_name = 'Адреса локации'
        verbose_name_plural = 'Адреса локаций'

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}'


class DeviceType(TimeModel):
    # Тип устройства Notebook, VDI fullClone, Printer
    name = models.CharField(
        db_index=True,
        max_length=60,
        verbose_name='Тип устройства'
    )

    class Meta:
        verbose_name = 'Тип устройства'
        verbose_name_plural = 'Типы устройств'

    def __str__(self):
        return self.name


class DeviceModel(TimeModel):
    model = models.TextField(
        db_index=True,
        verbose_name='Модель устройства'
    )
    note = models.CharField(
        max_length=60,
        verbose_name='Заметка по модели устройства',
        blank=True
    )
    device_type = models.ForeignKey(
        DeviceMonitoring,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип устройства взятого на мониторинг'
    )
    location = models.ForeignKey(
        LocationOffice,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Локация'
    )
    device_type_ref = models.ForeignKey(
        DeviceType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип устройства'
    )

    class Meta:
        verbose_name = 'Модель устройства'
        verbose_name_plural = 'Модели устройств'

    def __str__(self):
        return self.model
