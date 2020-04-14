from flask_restplus import Namespace, fields


class ReceiverDto:
    api = Namespace('receiver', description='workorder receiver related operations')
    receiver = api.model('receiver', {
        'work_orders': fields.String(required=True, description='Work Orders'),
    })

