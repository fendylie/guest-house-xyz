import app
import helpers.function_helper as FunctionHelper
import repositories.booking_repository as BookingRepository


def find_all():
    app.open_db_connection()
    data = []
    sql_query = "SELECT rooms.*, hotels.name as hotel_name FROM `rooms` LEFT JOIN hotels ON rooms.hotel_id = hotels.id"
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()

    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)


def find_one(id):
    app.open_db_connection()
    sql_query = "SELECT * FROM rooms WHERE id = " + str(id)
    app.cursor.execute(sql_query)
    result = app.cursor.fetchone()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Success Fetch Data", result)


def find_all_where_hotel(hotel_id):
    app.open_db_connection()
    data = []
    sql_query = "SELECT * FROM rooms WHERE hotel_id = " + str(hotel_id)
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()
    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)


def create(form):
    name = form.get('name')
    hotel_id = form.get('hotel_id')
    max_person = form.get('max_person')
    price = form.get('price')
    description = form.get('description')

    app.open_db_connection()
    sql_command = "INSERT INTO rooms (name, hotel_id, max_person, price, description) VALUES (%s, %s, %s, %s, %s)"
    value = (name, hotel_id, max_person, price, description)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Create Room")


def update(id, form):
    name = form.get('name')
    hotel_id = form.get('hotel_id')
    max_person = form.get('max_person')
    price = form.get('price')
    description = form.get('description')

    app.open_db_connection()
    sql_command = "UPDATE hotels SET name = %s, hotel_id = %s, max_person = %s, price = %s, description = %s WHERE id = " + str(id)
    value = (name, hotel_id, max_person, price, description)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Update Hotel")


def delete(id):
    find_hotel = find_one(id)
    find_room_in_booking = BookingRepository.find_all_where_room(id)

    # validasi apakah data room ini digunakan di database bookings
    if find_hotel['success'] and len(find_room_in_booking['data']) < 1:
        app.open_db_connection()
        sql_command = "DELETE FROM rooms WHERE id = " + str(id)
        app.cursor.execute(sql_command)
        app.conn.commit()
        app.close_db_connection()

        return FunctionHelper.response_formatter(True, "Successfully Delete Room")
    else:
        return FunctionHelper.response_formatter(False, "Failed Delete Room")


