import bcrypt
import repositories.user_repository as UserRepository
import repositories.room_repository as RoomRepository

def response_formatter(status, message, data=None):
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
    hashed_password = hash_password(input_password)
    return bcrypt.checkpw(hashed_password, password)


def get_user_choices():
    users = UserRepository.find_all_user()
    return [(user[0], user[2]) for user in users['data']]


def get_room_choices():
    rooms = RoomRepository.find_all()
    return [(room[0], room[2]) for room in rooms['data']]