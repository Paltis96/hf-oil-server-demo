from ..config import settings
from fastapi import HTTPException, status

import pymysql


def mysql_select(sql):
    connection = pymysql.connect(
        user=settings.db_user,
        password=settings.password,
        database=settings.database,
        host=settings.host,
        port=settings.port,
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
