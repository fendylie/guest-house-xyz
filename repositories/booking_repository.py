import app
import helpers.function_helper as FunctionHelper


def find_all():
    app.open_db_connection()
    data = []
    sql_query = "SELECT bookings.*, users.name as user_name, rooms.name as room_name, rooms.hotel_id as hotel_id, " \
                "hotels.name as hotel_name FROM bookings LEFT JOIN users ON bookings.user_id = users.id " \
                "LEFT JOIN rooms ON bookings.room_id = rooms.id LEFT JOIN hotels ON hotel_id = hotels.id"
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()

    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)


def find_one(id):
    app.open_db_connection()
    sql_query = "SELECT * FROM bookings WHERE id = " + str(id)
    app.cursor.execute(sql_query)
    result = app.cursor.fetchone()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Success Fetch Data", result)


def find_all_where_room(room_id):
    app.open_db_connection()
    data = []
    sql_query = "SELECT * FROM bookings WHERE room_id = " + str(room_id)
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()
    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)


def create(form):
    user_id = form.get('user_id')
    room_id = form.get('room_id')
    person = form.get('person')
    check_in = form.get('check_in')
    check_out = form.get('check_out')

    app.open_db_connection()
    sql_command = "INSERT INTO bookings (user_id, room_id, person, check_in, check_out) VALUES (%s, %s, %s, %s, %s)"
    value = (user_id, room_id, person, check_in, check_out)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Create Booking")


def update(id, form):
    user_id = form.get('user_id')
    room_id = form.get('room_id')
    person = form.get('person')
    check_in = form.get('check_in')
    check_out = form.get('check_out')

    app.open_db_connection()
    sql_command = "UPDATE bookings SET user_id = %s, room_id = %s, person = %s, check_in = %s, check_out = %s WHERE id = " + str(id)
    value = (user_id, room_id, person, check_in, check_out)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Update Booking")


def delete(id):
    find_booking = find_one(id)

    # validasi apakah data ada di database bookings
    if find_booking['success']:
        app.open_db_connection()
        sql_command = "DELETE FROM bookings WHERE id = " + str(id)
        app.cursor.execute(sql_command)
        app.conn.commit()
        app.close_db_connection()

        return FunctionHelper.response_formatter(True, "Successfully Delete Booking")
    else:
        return FunctionHelper.response_formatter(False, "Failed Delete Booking")



