import pymysql.cursors
from flask import Flask, render_template, request, redirect, session, flash
from forms.user_form import *
from forms.hotel_form import *
from forms.booking_form import *
from forms.room_form import *
from repositories.user_repository import *
import repositories.hotel_repository as HotelRepository
import repositories.room_repository as RoomRepository
from helpers.constant_helper import *


application = Flask(__name__)
application.secret_key = "loremipsum"
conn = cursor = None


def open_db_connection():
    global conn, cursor
    conn = pymysql.connect(host="localhost", user="root", password="", db="guest-house-xyz")
    cursor = conn.cursor()


# close database
def close_db_connection():
    global conn, cursor
    cursor.close()
    conn.close()


# Admin Route
# Admin Login Route
@application.route("/admin/login", methods=['GET', 'POST'])
def admin_login_route():
    form = UserLoginForm()
    session['email'] = request.form['email']
    return render_template("admin/login.html", form=form)


# Admin Booking Route
@application.route("/admin/booking", methods=['GET', 'POST'])
def admin_booking_route():
    list_booking = find_all_user()
    return render_template("admin/booking/list.html", data=list_booking)


# Admin Report Route
@application.route("/admin/report", methods=['GET'])
def admin_report_route():
    list_report = find_all_user()
    return render_template("admin/report/list.html", data=list_report)


# Admin Hotel Route
@application.route("/admin/hotel", methods=['GET'])
def admin_hotel_route():
    response = HotelRepository.find_all()
    return render_template("admin/hotel/list.html", data=response['data'])


# Admin Hotel Create Route
@application.route("/admin/hotel/create", methods=['GET', 'POST'])
def admin_hotel_create_route():
    form = HotelForm()

    if request.method == "POST":
        if form.validate():
            response = HotelRepository.create(request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/hotel")
            else:
                return render_template(ADMIN_HOTEL_CREATE_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_HOTEL_CREATE_TEMPLATE, form=form)

    return render_template(ADMIN_HOTEL_CREATE_TEMPLATE, form=form)


# Admin Hotel Edit Route
@application.route("/admin/hotel/<int:id>", methods=['GET', 'POST'])
def admin_hotel_edit_route(id):
    form = HotelForm()
    hotel = HotelRepository.find_one(id)

    if request.method == "POST":
        if form.validate():
            response = HotelRepository.update(id, request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/hotel")
            else:
                return render_template(ADMIN_HOTEL_EDIT_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_HOTEL_EDIT_TEMPLATE, form=form)

    return render_template(ADMIN_HOTEL_EDIT_TEMPLATE, form=form, hotel=hotel['data'])


# Admin Hotel Delete Route
@application.route("/admin/hotel/<int:id>/delete", methods=['GET'])
def admin_hotel_delete_route(id):
    response = HotelRepository.delete(id)
    if response['success']:
        flash(response['message'])
    else:
        flash(response['message'], "error")

    return redirect("/admin/hotel")


# Admin Room Route
@application.route("/admin/room", methods=['GET', 'POST'])
def admin_room_route():
    response = RoomRepository.find_all()
    return render_template("admin/room/list.html", data=response['data'])


# Admin Room Create Route
@application.route("/admin/room/create", methods=['GET', 'POST'])
def admin_room_create_route():
    form = RoomForm()
    hotels = HotelRepository.find_all()
    form.hotel_id.choices =  [(hotel[0], hotel[1]) for hotel in hotels['data']]

    if request.method == "POST":
        if form.validate():
            response = RoomRepository.create(request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/room")
            else:
                return render_template(ADMIN_ROOM_CREATE_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_ROOM_CREATE_TEMPLATE, form=form)

    return render_template(ADMIN_ROOM_CREATE_TEMPLATE, form=form)


# Admin Room Edit Route
@application.route("/admin/room/<int:id>", methods=['GET', 'POST'])
def admin_room_edit_route(id):
    form = RoomForm()
    room = RoomRepository.find_one(id)
    hotels = HotelRepository.find_all()
    find_hotel = HotelRepository.find_one(room['data'][1])
    form.hotel_id.choices = [(hotel[0], hotel[1]) for hotel in hotels['data']]

    if request.method == "POST":
        if form.validate():
            response = RoomRepository.update(id, request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/room")
            else:
                return render_template(ADMIN_ROOM_EDIT_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_ROOM_EDIT_TEMPLATE, form=form)

    # Data hotel tidak ter set
    form.hotel_id.data = find_hotel['data'][0]
    return render_template(ADMIN_ROOM_EDIT_TEMPLATE, form=form, room=room['data'])


# Admin Hotel Delete Route
@application.route("/admin/room/<int:id>/delete", methods=['GET'])
def admin_room_delete_route(id):
    response = RoomRepository.delete(id)
    if response['success']:
        flash(response['message'])
    else:
        flash(response['message'], "error")

    return redirect("/admin/room")


# Admin User Route
@application.route("/admin/user", methods=['GET', 'POST'])
def admin_user_route():
    list_user = find_all_user()
    print(list_user)

    return render_template("admin/list.html", data=list_user)

# End of Admin Route


# User Route
# User Login Route
@application.route("/login", methods=['GET', 'POST'])
def user_login_route():
    form = UserLoginForm()
    return render_template("user/login.html", form=form)


# User Register Route
@application.route("/register", methods=['GET', 'POST'])
def user_register_route():
    form = UserLoginForm()
    return render_template("user/register.html", form=form)

# End of User Route


if __name__ == '__main__':
    application.run(debug=True)

