from flask_restplus import Namespace, fields


class PipeDto:
    api = Namespace('pipe', description='redis pipeline related operations')
    api_model = api.model('pipe', {
        'datas': fields.String(required=True, description='Rredis Pipeline'),
    })

