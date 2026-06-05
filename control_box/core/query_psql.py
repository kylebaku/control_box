from django.db import connections, connection
import pandas as pd


def get_city_choices():
    """Получение списка городов из базы postgres_zbx"""
    choices = [('', 'Выберите город')]

    with connections['postgres_zbx'].cursor() as cursor:
        # Пример запроса - замените на вашу таблицу с городами
        cursor.execute("""
            select code_hd, filialrus  from ci_branch cb where status = '2'
        """)

        for row in cursor.fetchall():
            # row[0] - id (отправляемое значение)
            # row[1] - filialrus (отображаемый текст)
            choices.append((str(row[1]), row[1]))

    return choices


def get_role_choices():
    """Получение списка ролей из базы postgres_zbx"""
    choices = [('', 'Выберите роль')]

    with connections['postgres_zbx'].cursor() as cursor:
        # Пример запроса - замените на вашу таблицу с городами
        cursor.execute("""
            SELECT "Name", "code_hd"
            FROM dic_orgstructure do2
            WHERE "Name" LIKE '%ГЛТП'
            OR "Name" LIKE '%ВК'
        """)

        for row in cursor.fetchall():
            # row[0] - id (отправляемое значение)
            # row[1] - filialrus (отображаемый текст)
            choices.append((str(row[0]), row[0]))

    return choices


def get_triger_adm_sop(triger_name, triger_count):
    """
    Получение списка триггеров по условию полученному из задачи (postgres_zbx)
    вызывается функцией query_db_scheduler()
    """
    choices = []  # Убираем заголовки, оставляем только данные
    conn = connections['postgres_zbx']

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM (
                    SELECT
                        hostname,
                        COUNT(hostname) AS count_,
                        CASE
                            WHEN LENGTH(SPLIT_PART(hostname, '-', 1)) = 2 THEN 'false'
                            WHEN LENGTH(SPLIT_PART(hostname, '-', 1)) = 4 THEN
                                CASE
                                    WHEN SUBSTRING(SPLIT_PART(hostname, '-', 2) FROM 1 FOR 1) = 'S'
                                    THEN SPLIT_PART(hostname, '-', 2)
                                    ELSE 'false'
                                END
                            ELSE 'false'
                        END AS code_sop,
                        CASE
                            WHEN LENGTH(SPLIT_PART(hostname, '-', 1)) IN (2, 4)
                            THEN SPLIT_PART(hostname, '-', 1)
                            ELSE 'false'
                        END AS type,
                        problem_name,
                        CURRENT_DATE
                    FROM zabbix_trigger_adm
                    WHERE problem_name = %s
                        AND dtcreate >= date_trunc('day', CURRENT_TIMESTAMP - INTERVAL '7D')
                    GROUP BY hostname, problem_name, CURRENT_DATE
                    ORDER BY count_ DESC
                ) t1
                WHERE count_ >= %s
            """, (triger_name, triger_count))

            # Получаем результаты пока соединение открыто
            results = cursor.fetchall()

            # Формируем выборку
            for row in results:
                choices.append((row[0], row[1], row[2], row[3], row[4]))

    except Exception as e:
        print(f"Database error: {e}")
        choices = []  # В случае ошибки возвращаем пустой список
    finally:
        conn.close()

    return choices


class GetTriggeAdmSop:
    """Запрос данных триггеров из таблиц ADM и SOP и подготовка в целом
    данных для формирования ТТ"""

    def __init__(self, trigger_name, trigger_count):
        self.trigger_name = trigger_name
        self.trigger_count = trigger_count

    def serch_triger(self):
        """
        Получение списка триггеров по условию полученному из задачи (postgres_zbx)
        вызывается функцией query_db_scheduler()
        """
        conn = connections['postgres_zbx']
        try:
            df_trigger = pd.read_sql("""
                    SELECT * FROM (
                        SELECT 
                            hostname, 
                            COUNT(hostname) AS count_, 
                            CASE 
                                WHEN LENGTH(SPLIT_PART(hostname, '-', 1)) = 2 THEN 'false'
                                WHEN LENGTH(SPLIT_PART(hostname, '-', 1)) = 4 THEN 
                                    CASE 
                                        WHEN SUBSTRING(SPLIT_PART(hostname, '-', 2) FROM 1 FOR 1) = 'S' 
                                        THEN SPLIT_PART(hostname, '-', 2)
                                        ELSE 'false'
                                    END
                                ELSE 'false'
                            END AS code_sop,
                            CASE 
                                WHEN LENGTH(SPLIT_PART(hostname, '-', 1)) IN (2, 4) 
                                THEN LEFT(SPLIT_PART(hostname, '-', 1), 2) 
                                ELSE 'false'
                            END AS branch,
                            problem_name,
                            CURRENT_DATE
                        FROM zabbix_trigger_adm
                        WHERE problem_name = %s
                            AND dtcreate >= date_trunc('day', CURRENT_TIMESTAMP - INTERVAL '7D')
                        GROUP BY hostname, problem_name, CURRENT_DATE
                        ORDER BY count_ DESC
                    ) t1
                    WHERE count_ >= %s
                """, conn, params=(self.trigger_name, self.trigger_count))

        except Exception as e:
            print(f"Database error: {e}")
            df_trigger = pd.DataFrame()
        finally:
            conn.close()

        return df_trigger

    def serch_branch(self):
        """
        Функция чтения всех задач из БД для запуска шедуллера.
        """
        try:
            df_role = pd.read_sql("""
                SELECT *
                FROM generation_branchrole
            """, connection)
            df_branch = pd.read_sql("""
                SELECT *
                FROM generation_branchhd
            """, connection)
        except Exception as e:
            print(f"Database error: {e}")
            df_role = pd.DataFrame()  # Возвращаем пустой DataFrame при ошибке
            df_branch = pd.DataFrame()
        return df_branch, df_role

    def full_data_adm_sop(self):
        df_trigger = self.serch_triger()
        df_branch, df_role = self.serch_branch()
        
        df_merged = pd.merge(
            df_trigger,
            df_role,
            left_on='branch',      # поле из df_trigger
            right_on='branch_code',  # поле из df_role
            how='left'
        )
        
        df_merged = pd.merge(
            df_merged,
            df_branch,
            left_on='branch_city_en',      # или другое поле для связи
            right_on='filialrus',    # поле из df_branch (например code_hd)
            how='left'
        )
        
        self.df_merged = df_merged
        return self.df_merged
