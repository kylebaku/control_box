from django.db import connection
from background_task import background
from datetime import date, datetime
from core.query_psql import get_triger_admin_pc

@background
def query_db_scheduler():
    """
    Функция чтения всех задач из БД для запуска шедуллера.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT gs.user_create_schedule,
                ga.action_name,
                gd.monthly_schedule,
                gd.weekly_schedule,
                gd.time_schedule,
                gd.start_date,
                gn.name_schedule,
                gn.description_schedule,
                gr.name_rules,
                gr.count_rules,
                gr.month_over_month,
                gr.week_over_week,
                gr.day_over_day,
                gt.text_action
            FROM generation_scheduler gs
            LEFT JOIN generation_actionschedule ga ON gs.action_schedule_id = ga.id
            LEFT JOIN generation_datetimeschedule gd ON gs.date_time_schedule_id = gd.id
            LEFT JOIN generation_nameschedule gn ON gs.description_schedule_id = gn.id
            LEFT JOIN generation_rulesschedule gr ON gs.rules_schedule_id = gr.id
            LEFT JOIN generation_textaction gt ON gs.text_action_id = gt.id
        """)
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

    if len(result) > 0:
        for record in result:
            start_date = record.get('start_date')
            time_schedule = record.get('time_schedule')
            name_schedule = record.get('name_schedule', 'Unknown')
            weekly_schedule = record.get('weekly_schedule')
            today = date.today()
            now_time = datetime.now().time().replace(second=0, microsecond=0)
            schedule_time_clean = time_schedule.replace(second=0, microsecond=0)
            weekly = date.today().weekday()
            problem_name = record.get('name_rules')
            count_rules = record.get('count_rules')
            
            # Проверка, что данные существуют в таблицах (нет None)
            if start_date is None or time_schedule is None:
                print(
                    f"Пропуск: start_date или time_schedule = None "
                    f"для {name_schedule}"
                )
                return result
            
            # Если дата старта меньше текущей даты, время совпадает
            # и день недели совпадает, тогда запускаем скрипт
            if (start_date <= today 
                    and now_time == schedule_time_clean 
                    and str(weekly) in weekly_schedule):
                print('___________________________________________________________')
                print(
                    f"✅ {name_schedule}: дата {start_date} <= {today} "
                    f"и время совпадает ✅"
                )
                print(get_triger_admin_pc(problem_name, count_rules))
                print(problem_name, count_rules)
                # Здесь вызывайте нужное действие
            else:
                print(
                    f"⏳ {name_schedule}: дата {start_date} > {today} "
                    f"или время не совпадает ❌"
                )
                print(
                    f"today={today}, start_date={start_date}, "
                    f"now_time={now_time}, schedule={schedule_time_clean}"
                )
                print(
                    f'___________________________________________________________'
                    f'{weekly_schedule}, {weekly}'
                )
    
    return result
