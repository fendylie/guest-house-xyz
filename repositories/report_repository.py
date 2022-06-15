import app
from helpers.constant_helper import ROLE_USER, ROLE_ADMIN
import helpers.function_helper as FunctionHelper
import bcrypt


def find_all():
    app.open_db_connection()
    data = []
    sql_query = "SELECT * FROM users WHERE role = '" + ROLE_USER + "'"
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()
    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)

