from flask import request
from flask_restplus import Resource

from app.main.util.decorator import token_required
from ..util.dto import ReceiverDto
from ..service.receiver_service import ReceiverService

api = ReceiverDto.api
_receiver = ReceiverDto.receiver

_ReceiverService = ReceiverService()

@api.route('/')
class Receiver(Resource):
    @api.response(201, 'Work order successfully received.')
    @api.doc('receive a new work order')
    def post(self):
        """Creates a new User """
        data = request.json
        return _ReceiverService.save_new_workorder(data=data)

