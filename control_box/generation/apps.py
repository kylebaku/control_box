from django.apps import AppConfig


class GenerationConfig(AppConfig):
    name = 'generation'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # Функция запуска планировщика задач
        from .tasks import query_db_scheduler
        from background_task.models import Task, CompletedTask
        
        # Импорт обязательно в функции для избежания зацикливания
        task_name = 'generation.tasks.query_db_scheduler'
        Task.objects.filter(task_name=task_name).delete()
        
        # Полная очистка обеих таблиц перед стартом планировщика
        # в противном случае при каждом запуске будут накапливаться задачи,
        # которые будут дублировать (история выполнения задач и планировщик)
        # CompletedTask.objects.filter(task_name=task_name).delete()
        
        # Создаем новую задачу
        query_db_scheduler(schedule=6, repeat=6)