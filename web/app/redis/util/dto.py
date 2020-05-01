from flask_restplus import Namespace, fields


class QueueDto:
    api = Namespace('queue', description='redis queue related operations')
    api_model = api.model('queue', {
        'datas': fields.String(required=True, description='Redis Queue'),
    })

