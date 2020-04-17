from flask import request
from flask_restplus import Resource

from ..util.dto import PipeDto
from ..service.pipe_service import SampleQueue


api = PipeDto.api
_api_model = PipeDto.api_model
_SampleQueue = SampleQueue()

@api.route('/add')
class PipeAdd(Resource):
    @api.response(201, 'Data successfully received in redis.')
    @api.doc('receive a new data in redis')
    def post(self) -> dict:
        """
        Recieve and add data to redis pipeline

        :returns:   Api reponse
        :rtype:     dict
        """
        data = request.json
        return _SampleQueue.save_data(data=data)


@api.route('/read')
class PipeAdd(Resource):
    @api.response(201, 'Data successfully read in redis.')
    @api.doc('reads datas in redis from head')
    def get(self) -> list:
        """
        get's all the data in redis pipeline

        :returns:   Api reponse
        :rtype:     list
        """
        total_count = request.args.get('total_count', 1)
        return _SampleQueue.get_from_head(total_count)



@api.route('/flush')
class PipeAdd(Resource):
    @api.response(201, 'Data successfully flush in redis.')
    @api.doc('flush all datas in redis')
    def get(self) -> dict:
        """
        flush all data

        :returns:   Api reponse
        :rtype:     dict
        """
        return _SampleQueue.flushall()

