import uuid
import datetime

def save_new_workorder(data):
    response_object = {
        'status': 'success',
        'message': 'Successfully received.',
        'data' : data,
    }
    return response_object, 201

class ReceiverService(object):
    """docstring for ReceiverService """
    def __init__(self):
        super(ReceiverService, self).__init__()

    def save_new_workorder(self, data):
        response_object = {
            'status': 'success',
            'message': 'Successfully received.',
            'data' : data,
        }
        return response_object, 201