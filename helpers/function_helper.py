def response_formatter(status, message, data=[]):
    response = dict()
    response['success'] = status
    response['message'] = message
    response['data'] = data

    return response
