from django.db import connections

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

def get_triger_admin_pc(triger_name, triger_count):
    """
    Получение списка тригерв по условию полченному из задачи (postgres_zbx)
    вызывается вункцией query_db_scheduler()
    """
    choices = [('hostname', 'count','code_sop','problem_name','current_date')]
    conn = connections['postgres_zbx']
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    hostname,
                    COUNT(hostname) AS count_,
                    SUBSTRING(hostname FROM 5 FOR 6) AS code_sop,
                    problem_name,
                    CURRENT_DATE
                FROM zabbix_trigger_adm
                WHERE problem_name LIKE %s
                    AND dtcreate >= DATE_TRUNC('day', CURRENT_TIMESTAMP - INTERVAL '7D')
                GROUP BY
                    hostname,
                    problem_name,
                    CURRENT_DATE
                HAVING COUNT(hostname) >= %s
                ORDER BY count_ DESC
            """, (f'%{triger_name}%', triger_count))
            for row in cursor.fetchall():
                # row[0] - hostname
                # row[1] - count  
                # row[2] - code_sop
                # row[3] - problem_name
                # row[4] - current_date
                choices.append((row[0], row[1], row[2], row[3], row[4]))
    finally:
        conn.close()

    return choices
