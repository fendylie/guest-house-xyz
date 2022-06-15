import app
import helpers.function_helper as FunctionHelper


def login_admin(form):
    email = form.get("email")
    password = form.get("password")

    app.open_db_connection()
    sql_query = "SELECT * FROM users WHERE email = '" + email + "' AND role = 'ADMIN'"
    app.cursor.execute(sql_query)
    result = app.cursor.fetchone()
    app.close_db_connection()

    if result is not None:
        if FunctionHelper.valid_password(password, result[4]):
            return FunctionHelper.response_formatter(True, "Successfully Login", result)
        else:
            return FunctionHelper.response_formatter(False, "Email or password is wrong")
    else:
        return FunctionHelper.response_formatter(False, "User Not Found")

