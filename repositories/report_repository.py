import app
import helpers.function_helper as FunctionHelper


def find_all():
    app.open_db_connection()
    data = []
    sql_query = "select users.id, users.name, users.email, users.phone_number, sum(rooms.price) as total_expense, " \
                "count(bookings.id) as total_book, sum(DATEDIFF(bookings.check_out,bookings.check_in)) as total_book_day " \
                "from bookings join users on users.id = bookings.user_id " \
                "join rooms on rooms.id = bookings.room_id GROUP BY users.id"
    app.cursor.execute(sql_query)
    results = app.cursor.fetchall()
    app.close_db_connection()
    if results is not None:
        for item in results:
            data.append(item)

    return FunctionHelper.response_formatter(True, "Success Fetch Data", data)

