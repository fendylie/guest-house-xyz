import app
from helpers.constant_helper import ROLE_USER, ROLE_ADMIN
import helpers.function_helper as FunctionHelper


def find_all_user():
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


def find_one(id):
    app.open_db_connection()
    sql_query = "SELECT * FROM users WHERE id = " + str(id)
    app.cursor.execute(sql_query)
    result = app.cursor.fetchone()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Success Fetch Data", result)


def find_one_by_email(email):
    app.open_db_connection()
    sql_query = "SELECT * FROM users WHERE email = '" + email + "'"
    app.cursor.execute(sql_query)
    result = app.cursor.fetchone()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Success Fetch Data", result)


def find_all_admin():
    app.open_db_connection()
    data = []
    sql_query = "SELECT * FROM users WHERE role = " + ROLE_ADMIN
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()
    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)


def create(form):
    name = form.get('name')
    phone_number = form.get('phone_number')
    email = form.get('email')
    password = FunctionHelper.hash_password(form.get('password'))

    app.open_db_connection()
    sql_command = "INSERT INTO users (name, phone_number, email, password, role) VALUES (%s, %s, %s, %s, %s)"
    value = (name, phone_number, email, password, "USER")
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Create Hotel")


def update(id, form):
    name = form.get('name')
    phone_number = form.get('phone_number')
    email = form.get('email')

    app.open_db_connection()
    sql_command = "UPDATE users SET name = %s, phone_number = %s, email = %s WHERE id = " + str(id)
    value = (name, phone_number, email)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Update User")


def update_from_user(id, form):
    name = form.get('name')
    phone_number = form.get('phone_number')
    email = form.get('email')

    app.open_db_connection()
    sql_command = "UPDATE users SET name = %s, phone_number = %s, email = %s WHERE id = " + str(id)
    value = (name, phone_number, email)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Update Profile")


def delete(id):
    find_user = find_one(id)

    if find_user['success']:
        # delete data user from database users
        app.open_db_connection()
        sql_command = "DELETE FROM users WHERE id = " + str(id)
        app.cursor.execute(sql_command)

        # delete data user from database bookings
        sql_command_booking = "DELETE FROM bookings WHERE user_id = " + str(id)
        app.cursor.execute(sql_command_booking)

        app.conn.commit()
        app.close_db_connection()

        return FunctionHelper.response_formatter(True, "Successfully Delete User")
    else:
        return FunctionHelper.response_formatter(False, "Failed Delete User")

