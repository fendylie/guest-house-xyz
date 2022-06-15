import bcrypt
import repositories.user_repository as UserRepository
import repositories.room_repository as RoomRepository

def response_formatter(status, message, data=None):
    # response formatter api
    response = dict()
    response['success'] = status
    response['message'] = message
    response['data'] = data

    return response


def hash_password(password):
    # Encode password
    encode_password = password.encode('utf-8')
    # Return Hash password
    return bcrypt.hashpw(encode_password, bcrypt.gensalt())


def valid_password(input_password, password):
    # validasi password
    encode_password = input_password.encode("utf-8")
    return bcrypt.checkpw(encode_password, password.encode("utf-8"))


def get_user_choices():
    # ambil data user dari database
    users = UserRepository.find_all_user()
    return [(user[0], user[2]) for user in users['data']]


def get_room_choices():
    # ambil data room dari database
    rooms = RoomRepository.find_all()
    return [(room[0], room[2]) for room in rooms['data']]


def get_room_choices_by_hotel(id):
    # ambil data room dari database
    rooms = RoomRepository.find_all_where_hotel(id)
    return [(room[0], room[2]) for room in rooms['data']]


