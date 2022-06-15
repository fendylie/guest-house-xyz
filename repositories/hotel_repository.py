import app
import helpers.function_helper as FunctionHelper
import repositories.room_repository as RoomRepository


def find_all():
    app.open_db_connection()
    data = []
    sql_query = "SELECT * FROM hotels"
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()
    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)


def find_one(id):
    app.open_db_connection()
    sql_query = "SELECT * FROM hotels WHERE id = " + str(id)
    app.cursor.execute(sql_query)
    result = app.cursor.fetchone()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Success Fetch Data", result)


def create(form):
    name = form.get('name')
    phone_number = form.get('phone_number')
    location = form.get('location')
    rating = form.get('rating')

    app.open_db_connection()
    sql_command = "INSERT INTO hotels (name, phone_number, location, rating) VALUES (%s, %s, %s, %s)"
    value = (name, phone_number, location, rating)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Create Hotel")


def update(id, form):
    name = form.get('name')
    phone_number = form.get('phone_number')
    location = form.get('location')
    rating = form.get('rating')

    app.open_db_connection()
    sql_command = "UPDATE hotels SET name = %s, phone_number = %s, location = %s, rating = %s WHERE id = " + str(id)
    value = (name, phone_number, location, rating)
    app.cursor.execute(sql_command, value)
    app.conn.commit()
    app.close_db_connection()

    return FunctionHelper.response_formatter(True, "Successfully Update Hotel")


def delete(id):
    find_hotel = find_one(id)
    find_hotel_in_room = RoomRepository.find_all_where_hotel(id)

    # validasi apakah data hotel ini digunakan di database rooms
    if find_hotel['success'] and len(find_hotel_in_room['data']) < 1:
        app.open_db_connection()
        sql_command = "DELETE FROM hotels WHERE id = " + str(id)
        app.cursor.execute(sql_command)
        app.conn.commit()
        app.close_db_connection()

        return FunctionHelper.response_formatter(True, "Successfully Delete Hotel")
    else:
        return FunctionHelper.response_formatter(False, "Failed Delete Hotel, Check if this data is used on your transaction")

