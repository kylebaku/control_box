from django.db import models

#имя условия
class NameSchedule(models.Model):
    name_schedule = models.CharField(
        '',
        blank=False,
        max_length=50
    )
    description_schedule = models.TextField(
        'Описание правила'
    )

    def __str__(self):
        return self.name_schedule or f"Rule #{self.id}"

    class Meta:
        verbose_name = 'Имя правила'
        verbose_name_plural = 'Имена правил'

#Дата и время расписания.
class DateTimeSchedule(models.Model):
    """Дата и время расписания."""
    monthly_schedule = models.CharField('')
    weekly_schedule = models.CharField('')
    time_schedule = models.TimeField('')
    start_date = models.DateField('')

    def __str__(self):
        return f"{self.monthly_schedule} | {self.time_schedule}"

    class Meta:
        verbose_name = 'Дата и время расписания'
        verbose_name_plural = 'Даты и время расписаний'

#Текстовое сообщение при возникновении срабатывания задачи
class TextAction(models.Model):
    """Текстовое сообщение при возникновении срабатывания задачи."""
    text_action = models.TextField('Детальное описание')

    def __str__(self):
        return self.text_action[:50]

    class Meta:
        verbose_name = 'Тип действия'
        verbose_name_plural = 'Типы действий'

#Тип задачи планировщика ТТ, почта, buzz.
class ActionSchedule(models.Model):
    """Тип задачи планировщика ТТ, почта, buzz."""
    action_name = models.CharField(
        'Тип оповещения о событии',
        max_length=55
    )

    def __str__(self):
        return self.action_name

    class Meta:
        verbose_name = 'Тип попвещений задач'
        verbose_name_plural = 'Типы оповещений'

#Правила срабатывания задачи.
class RulesSchedule(models.Model):
    """Правила срабатывания задачи."""
    name_rules = models.CharField(
        'Выберите условие',
        max_length=50
    )
    count_rules = models.IntegerField(null=True, blank=False)
    month_over_month = models.IntegerField(null=True, blank=False)
    week_over_week = models.IntegerField(null=True, blank=False)
    day_over_day = models.IntegerField(null=True, blank=False)
    
    def __str__(self):
        return self.name_rules

    class Meta:
        verbose_name = 'Правило расписания'
        verbose_name_plural = 'Правила расписаний'

#Основной планировщик задачи.
class Scheduler(models.Model):
    """Основной планировщик."""
    user_create_schedule = models.CharField(
        'Инициатор правила',
        max_length=50,
        default=''
    )
    description_schedule = models.ForeignKey(
        NameSchedule,
        on_delete=models.CASCADE,
        verbose_name='Описание условия планировщика'
    )
    date_time_schedule = models.ForeignKey(
        DateTimeSchedule,
        on_delete=models.CASCADE,
        verbose_name='Расписание планировщика',
        default=None
    )
    action_schedule = models.ForeignKey(
        ActionSchedule,
        on_delete=models.CASCADE,
        verbose_name='Тип оповещения планировщика',
        default=None
    )
    rules_schedule = models.ForeignKey(
        RulesSchedule,
        on_delete=models.CASCADE,
        verbose_name='Выберите правило срабатывания планировщика',
        default=None
    )

    text_action = models.ForeignKey(
        TextAction,
        on_delete=models.CASCADE,
        verbose_name='Текст сообщения при срабатывании',
        blank=True
    )

    def __str__(self):
        return f"Scheduler #{self.id} - {self.user_create_schedule}"
    
    def delete(self, *args, **kwargs):
        name_schedule = self.description_schedule
        datetime_schedule = self.date_time_schedule
        rules_schedule = self.rules_schedule
        text_action = self.text_action

        super().delete(*args, **kwargs)

        if name_schedule:
            name_schedule.delete()
        if datetime_schedule:
            datetime_schedule.delete()
        if rules_schedule:
            rules_schedule.delete()
        if text_action:
            text_action.delete()

    class Meta:
        db_table = 'generation_scheduler'
        verbose_name = 'Планировщик'
        verbose_name_plural = 'Планировщики'

###############################################################
#Зарпос в БД
###############################################################
class ProblemName(models.Model):
    index = models.BigIntegerField(primary_key=True) 
    problem_name = models.TextField(db_column='problem_name')
    # category_type = models.TextField(db_column='Category_Type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zabbix_trigger_adm'

    def __str__(self):
        return str(self.__dict__)