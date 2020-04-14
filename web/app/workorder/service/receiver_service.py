import uuid
import datetime

def save_new_workorder(data):
    response_object = {
        'status': 'success',
        'message': 'Successfully received.',
        'data' : data,
    }
    return response_object, 201
