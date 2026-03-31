from django.db import models


class TimeModel(models.Model):
    # Базовая модел для хранения даты создаия и изменения записей таблиц
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True
