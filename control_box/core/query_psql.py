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
    """Получение списка городов из базы postgres_zbx"""
    choices = [('', 'Выберите город')]
    
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