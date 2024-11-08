import pymysql.cursors
from flask import Flask, render_template, request, redirect, session, flash
from flask_mail import Mail, Message
from forms.user_form import *
from forms.hotel_form import *
from forms.booking_form import *
from forms.room_form import *
import repositories.user_repository as UserRepository
import repositories.hotel_repository as HotelRepository
import repositories.room_repository as RoomRepository
import repositories.booking_repository as BookingRepository
import repositories.report_repository as ReportRepository
import repositories.auth_repository as AuthRepository

import helpers.function_helper as FunctionHelper
from helpers.constant_helper import *
import os
import convertapi

application = Flask(__name__)
application.secret_key = "loremipsum"

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'crazydefense2777@gmail.com',
    "MAIL_PASSWORD": 'auoyrrnzphngzwra'
}

application.config.update(mail_settings)
mail = Mail(application)

conn = cursor = None

# for sending email
@application.route("/sendemail/<int:user_id>")
def send_email(user_id):
    # read user
    user = UserRepository.find_one(user_id);

    # make message email
    msg = Message(
        'LIMITED OFFERING',
        sender ='crazydefense2777@gmail.com',
        recipients = [user["data"][1]]
    )

    # render template to email
    msg.html  = render_template(
        EMAIL_TEMPLATE,
        title="Check this offering right now " + user["data"][2],
        paragraph="Book Guest Houses Online. No reservation costs. Great rates. Get Instant Confirmation. Read Real Guest Reviews. No Booking Fees. Best Price Guarantee. 24/7 Customer Service."
    )

    # send email
    mail.send(msg)

    flash("Successfull send email to " + user["data"][1])
    return redirect("/admin/user")

# open db connection
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
@application.route("/admin", methods=['GET'])
def admin_index_route():
    return redirect("/admin/login")


# Admin Login Route
@application.route("/admin/login", methods=['GET', 'POST'])
def admin_login_route():
    # check user is admin and have session login
    if session.get("email") and session.get("role") == "ADMIN":
        return redirect("/admin/booking")

    # initial flask form
    form = UserLoginForm()

    # check request method is POST
    if request.method == "POST":
        # validasi form
        if form.validate():
            # call api login admin
            response = AuthRepository.login_admin(request.form)
            # cek apakah user ada atau tidak
            if response['success']:
                # set session email dan role
                session['email'] = response['data'][1]
                session['role'] = "ADMIN"
                # redirect ke booking page
                return redirect("/admin/booking")
            else:
                return render_template(ADMIN_LOGIN_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_LOGIN_TEMPLATE, form=form)

    return render_template(ADMIN_LOGIN_TEMPLATE, form=form)


# Logout Route
@application.route("/admin/logout", methods=['GET', 'POST'])
def admin_logout_route():
    # admin logout and remove session
    session.pop("email", None)
    session.pop("role", None)
    return redirect("/admin/login")


# Admin Report Route
@application.route("/admin/report", methods=['GET'])
def admin_report_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # get report from database
    response = ReportRepository.find_all()
    # get user from database
    users = FunctionHelper.get_user_choices()
    # set user selected if has on url params
    args = request.args
    selected_user = args.get("user") if args.get("user") else "0"

    if selected_user != "0":
        temp_data = []
        for user in response['data']:
            if str(user[0]) == str(selected_user):
                temp_data.append(user)

        response['data'] = temp_data

    return render_template(ADMIN_REPORT_LIST_TEMPLATE, data=response['data'], users=users, selected_user=int(selected_user))


# Admin Report Export Route
@application.route("/admin/report/export", methods=['GET', 'POST'])
def admin_report_export_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # get report from database
    response = ReportRepository.find_all()
    # get user from database
    users = FunctionHelper.get_user_choices()

    # set user selected if has on url params
    args = request.args
    selected_user = args.get("user") if args.get("user") else "0"

    if selected_user != "0":
        temp_data = []
        for user in response['data']:
            if str(user[0]) == str(selected_user):
                temp_data.append(user)

        response['data'] = temp_data

    # convertapi secret key
    convertapi.api_secret = 'HeQOuUbO4wL08bTa'

    # membuat file temp untuk menampung render template
    with open("temp.html", "w") as fo:
        fo.write(render_template(ADMIN_REPORT_LIST_TEMPLATE, data=response['data'], users=users, selected_user=int(selected_user)))

    # convert temp html to pdf using convertapi
    convertapi.convert('pdf', {
        'File': os.path.realpath('.') + '/temp.html'
    }, from_format='html').save_files(os.path.realpath('.') + '/static/pdf/report/report.pdf')

    # remove file temp
    os.remove(os.path.realpath('.') + '/temp.html')

    return redirect("/admin/report")


# Admin Booking Route
@application.route("/admin/booking", methods=['GET', 'POST'])
def admin_booking_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # get data booking dari database
    response = BookingRepository.find_all()
    return render_template(ADMIN_BOOKING_LIST_TEMPLATE, data=response['data'])


# Admin Booking Create Route
@application.route("/admin/booking/create", methods=['GET', 'POST'])
def admin_booking_create_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = BookingForm()
    # Get data user and set user choices
    form.user_id.choices = FunctionHelper.get_user_choices()
    # Get data room and set room choices
    form.room_id.choices =FunctionHelper.get_room_choices()

    if request.method == "POST":
        # validasi form
        if form.validate():
            # call create booking api
            response = BookingRepository.create(request.form)
            # cek apakah success atau tidak
            if response['success']:
                # redirect dan send flash message
                flash(response['message'])
                return redirect("/admin/booking")
            else:
                return render_template(ADMIN_BOOKING_CREATE_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_BOOKING_CREATE_TEMPLATE, form=form)

    return render_template(ADMIN_BOOKING_CREATE_TEMPLATE, form=form)


# Admin Booking Edit Route
@application.route("/admin/booking/<int:id>", methods=['GET', 'POST'])
def admin_booking_edit_route(id):
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = BookingForm()

    # get booking, user and room data from database
    booking = BookingRepository.find_one(id)
    # call api room dan user berdasarkan data booking
    find_user = UserRepository.find_one(booking['data'][1])
    find_room = RoomRepository.find_one(booking['data'][2])
    # Get data user and set user choices
    form.user_id.choices = FunctionHelper.get_user_choices()
    # Get data room and set room choices
    form.room_id.choices =FunctionHelper.get_room_choices()

    if request.method == "POST":
        if form.validate():
            response = BookingRepository.update(id, request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/booking")
            else:
                return render_template(ADMIN_BOOKING_EDIT_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_BOOKING_EDIT_TEMPLATE, form=form, booking=booking['data'])

    # set value user and room select
    form.user_id.data = find_user['data'][0]
    form.room_id.data = find_room['data'][0]

    return render_template(ADMIN_BOOKING_EDIT_TEMPLATE, form=form, booking=booking['data'])


# Admin Booking Delete Route
@application.route("/admin/booking/<int:id>/delete", methods=['GET'])
def admin_booking_delete_route(id):
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # call api delete booking
    response = BookingRepository.delete(id)
    # cek apakah delete success atau tidak
    if response['success']:
        flash(response['message'])
    else:
        flash(response['message'], "error")

    return redirect("/admin/booking")


# Admin Hotel Route
@application.route("/admin/hotel", methods=['GET'])
def admin_hotel_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    response = HotelRepository.find_all()
    return render_template(ADMIN_HOTEL_LIST_TEMPLATE, data=response['data'])


# Admin Hotel Create Route
@application.route("/admin/hotel/create", methods=['GET', 'POST'])
def admin_hotel_create_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = HotelForm()

    if request.method == "POST":
        if form.validate():
            # call api create hotel
            response = HotelRepository.create(request.form)
            # cek apakah create berhasil atau tidak
            if response['success']:
                # jika berhasil redirect ke hotel dan kirim flash message
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
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = HotelForm()
    # get hotel base on id from database
    hotel = HotelRepository.find_one(id)

    if request.method == "POST":
        # validasi form
        if form.validate():
            # call api update hotel
            response = HotelRepository.update(id, request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/hotel")
            else:
                return render_template(ADMIN_HOTEL_EDIT_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_HOTEL_EDIT_TEMPLATE, form=form, hotel=hotel['data'])

    return render_template(ADMIN_HOTEL_EDIT_TEMPLATE, form=form, hotel=hotel['data'])


# Admin Hotel Delete Route
@application.route("/admin/hotel/<int:id>/delete", methods=['GET'])
def admin_hotel_delete_route(id):
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # call api delete hotel
    response = HotelRepository.delete(id)
    if response['success']:
        flash(response['message'])
    else:
        flash(response['message'], "error")

    return redirect("/admin/hotel")


# Admin Room Route
@application.route("/admin/room", methods=['GET', 'POST'])
def admin_room_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # call api get room from database
    response = RoomRepository.find_all()
    return render_template("admin/room/list.html", data=response['data'])


# Admin Room Create Route
@application.route("/admin/room/create", methods=['GET', 'POST'])
def admin_room_create_route():
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = RoomForm()
    # get data hotel dan set ke choices
    hotels = HotelRepository.find_all()
    form.hotel_id.choices =  [(hotel[0], hotel[1]) for hotel in hotels['data']]

    if request.method == "POST":
        if form.validate():
            # call api create room
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
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = RoomForm()
    # get room by id
    room = RoomRepository.find_one(id)

    # get data hotel dan set ke hotel choices
    hotels = HotelRepository.find_all()
    find_hotel = HotelRepository.find_one(room['data'][1])
    form.hotel_id.choices = [(hotel[0], hotel[1]) for hotel in hotels['data']]

    # set hotel and description data
    form.hotel_id.data = find_hotel['data'][0]
    form.description.data = room['data'][5]

    if request.method == "POST":
        if form.validate():
            # call api update room
            response = RoomRepository.update(id, request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/room")
            else:
                return render_template(ADMIN_ROOM_EDIT_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_ROOM_EDIT_TEMPLATE, form=form, room=room['data'])

    return render_template(ADMIN_ROOM_EDIT_TEMPLATE, form=form, room=room['data'])


# Admin Hotel Delete Route
@application.route("/admin/room/<int:id>/delete", methods=['GET'])
def admin_room_delete_route(id):
    # check user is admin and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # call api delete
    response = RoomRepository.delete(id)
    if response['success']:
        flash(response['message'])
    else:
        flash(response['message'], "error")

    return redirect("/admin/room")


# Admin User Route
@application.route("/admin/user", methods=['GET', 'POST'])
def admin_user_route():
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # call api get user
    response = UserRepository.find_all_user()
    return render_template(ADMIN_USER_LIST_TEMPLATE, data=response['data'])


# Admin User Create Route
@application.route("/admin/user/create", methods=['GET', 'POST'])
def admin_user_create_route():
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = UserRegisterForm()

    if request.method == "POST":
        # validasi form
        if form.validate():
            # call api create user
            response = UserRepository.create(request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/user")
            else:
                return render_template(ADMIN_USER_CREATE_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_USER_CREATE_TEMPLATE, form=form)

    return render_template(ADMIN_USER_CREATE_TEMPLATE, form=form)


# Admin User Edit Route
@application.route("/admin/user/<int:id>", methods=['GET', 'POST'])
def admin_user_edit_route(id):
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    form = UserProfileForm()
    # get user by id
    user = UserRepository.find_one(id)

    if request.method == "POST":
        # validasi form
        if form.validate():
            # call api update user
            response = UserRepository.update(id, request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/admin/user")
            else:
                return render_template(ADMIN_USER_EDIT_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(ADMIN_USER_EDIT_TEMPLATE, form=form, user=user['data'])

    return render_template(ADMIN_USER_EDIT_TEMPLATE, form=form, user=user['data'])


# Admin User Delete Route
@application.route("/admin/user/<int:id>/delete", methods=['GET'])
def admin_user_delete_route(id):
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "ADMIN":
        return redirect("/admin/login")

    # call api delete user
    response = UserRepository.delete(id)
    if response['success']:
        flash(response['message'])
    else:
        flash(response['message'], "error")

    return redirect("/admin/user")


# User Route
# User Login Route
@application.route("/login", methods=['GET', 'POST'])
def user_login_route():
    # check user is user and have session login
    if session.get("email") and session.get("role") == "USER":
        return redirect("/")

    form = UserLoginForm()

    if request.method == "POST":
        if form.validate():
            # call api user login
            response = AuthRepository.login_user(request.form)
            if response['success']:
                # jika success set session email dan role
                session['email'] = response['data'][1]
                session['role'] = "USER"
                return redirect("/")
            else:
                return render_template(USER_LOGIN_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(USER_LOGIN_TEMPLATE, form=form)

    return render_template("user/login.html", form=form)


# User Register Route
@application.route("/register", methods=['GET', 'POST'])
def user_register_route():
    # check user is user and have session login
    if session.get("email") and session.get("role") == "USER":
        return redirect("/")

    form = UserRegisterForm()

    if request.method == "POST":
        # form validasi
        if form.validate():
            # create user from database
            response = UserRepository.create(request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/login")
            else:
                return render_template(USER_REGISTER_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(USER_REGISTER_TEMPLATE, form=form)

    return render_template(USER_REGISTER_TEMPLATE, form=form)


# Index Route
@application.route("/", methods=['GET'])
def index():
    # get hotel data from database
    hotels = HotelRepository.find_all()
    return render_template(USER_HOME_TEMPLATE, hotel=hotels['data'])


# User Booking Route
@application.route("/your-booking", methods=['GET'])
def user_booking_route():
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "USER":
        return redirect("/login")

    # get user by email
    get_user = UserRepository.find_one_by_email(session['email'])['data']
    # get booking by user
    bookings = BookingRepository.find_all_by_user(get_user[0])
    return render_template(USER_BOOKING_TEMPLATE, data=bookings['data'])


# User Booking Delete Route
@application.route("/your-booking/<int:id>/delete", methods=['GET'])
def user_booking_delete_route(id):
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "USER":
        return redirect("/login")

    # call api booking delete
    response = BookingRepository.delete(id)
    if response['success']:
        flash(response['message'])
    else:
        flash(response['message'], "error")

    return redirect("/your-booking")


# User Booking Hotel Route
@application.route("/booking-hotel/<int:id>", methods=['GET', 'POST'])
def user_booking_hotel_route(id):
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "USER":
        return redirect("/login")

    form = UserBookingForm()
    # get user by email
    get_user = UserRepository.find_one_by_email(session['email'])['data']
    # set room choices by hotel id from database
    form.room_id.choices = FunctionHelper.get_room_choices_by_hotel(id)
    # set user id base on user yang sedang login

    if request.method == "POST":
        # validasi flask form
        if form.validate():
            # call api create booking
            response = BookingRepository.create_from_user(request.form, get_user[0])
            if response['success']:
                flash(response['message'])
                return redirect("/")
            else:
                return render_template(USER_BOOKING_HOTEL_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(USER_BOOKING_HOTEL_TEMPLATE, form=form)

    return render_template(USER_BOOKING_HOTEL_TEMPLATE, form=form)


# User Profile Route
@application.route("/profile", methods=['GET', 'POST'])
def user_profile_route():
    # check user is user and have session login
    if not session.get("email") and session.get("role") != "USER":
        return redirect("/login")

    form = UserProfileForm()
    # get user by email from database
    user = UserRepository.find_one_by_email(session.get("email"))

    if request.method == "POST":
        if form.validate():
            # call api update user
            response = UserRepository.update_from_user(user['data'][0], request.form)
            if response['success']:
                flash(response['message'])
                return redirect("/")
            else:
                return render_template(USER_PROFILE_TEMPLATE, form=form, error_message=response['message'])
        else:
            return render_template(USER_PROFILE_TEMPLATE, form=form)

    return render_template(USER_PROFILE_TEMPLATE, form=form, user=user['data'])


# Logout Route
@application.route("/logout", methods=['GET', 'POST'])
def user_logout_route():
    # user logout and remove session
    session.pop("email", None)
    session.pop("role", None)
    return redirect("/login")
# End of User Route


if __name__ == '__main__':
    application.run(debug=True)

