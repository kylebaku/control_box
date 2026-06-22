from django.db import connection
from django.conf import settings
from background_task import background
from datetime import date, datetime
from core.query_psql import query_db_scheduler, GetTriggeAdmSop
import pandas as pd
import sqlite3

original_max_rows = pd.get_option('display.max_rows')
original_max_columns = pd.get_option('display.max_columns')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


@background(schedule=60)
def scheduler_trigger_adm_sop():
    result = query_db_scheduler()
    if len(result) > 0:
        for record in result:
            start_date = record.get('start_date')
            time_schedule = record.get('time_schedule')
            name_schedule = record.get('name_schedule', 'Unknown')
            weekly_schedule = record.get('weekly_schedule')
            device_type = record.get('device_type')
            today = date.today()
            now_time = datetime.now().time().replace(second=0, microsecond=0)
            schedule_time_clean = time_schedule.replace(
                second=0,
                microsecond=0
                )
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
                
                df_trigger = pd.DataFrame(result)
                df = GetTriggeAdmSop(
                    problem_name,
                    count_rules,
                    device_type
                    ).full_data_adm_sop()
                df_ti_sql_incert = pd.merge(
                    df, df_trigger,
                    left_on='problem_name',
                    right_on='name_rules'
                    )
                db_path = settings.DATABASES['default']['NAME']
                conn = sqlite3.connect(db_path)
                select_db_tt = (pd.read_sql('SELECT * FROM trigger_results', conn)).query("status_tt == 'unresolved'")  # все ранее созданные и записанные триггеры в БД отсавляем толькр нерещенные         
                # Делаем слияние, чтобы найти новые записи
                df_ = select_db_tt.merge(df_ti_sql_incert, on=['hostname', 'problem_name'], how='right', indicator=True)
                # Удаляем столбец _merge
                result_df = df_[df_['_merge'] == 'right_only'].drop('_merge', axis=1)
                # Оставляем только нужные столбцы из правой таблицы (новые данные)
                # Удаляем все столбцы с суффиксом _x (это данные из БД, которые не совпали)
                cols_to_keep = [col for col in result_df.columns if not col.endswith('_x')]
                # Переименовываем столбцы с суффиксом _y обратно (убираем суффикс)
                result_df = result_df[cols_to_keep]
                result_df.columns = [col.replace('_y', '') if col.endswith('_y') else col for col in result_df.columns]
                result_df.to_sql('trigger_results', conn, if_exists='append', index=False)
                conn.close()
                # Настройка pandas для построчного вывода
                with pd.option_context(
                    'display.max_rows', None,
                    'display.max_columns', None,
                    'display.width', 1000,
                    'display.expand_frame_repr', False  # Не переносить строки
                ):

                    print(df_)
                    df_.to_csv('df_.csv', index=False, encoding='utf-8-sig')
                    result_df.to_csv('result_df.csv', index=False, encoding='utf-8-sig')
                    select_db_tt.to_csv('select_db_tt.csv', index=False, encoding='utf-8-sig')
                    break
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

