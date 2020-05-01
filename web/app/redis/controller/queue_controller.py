from flask import request
from flask_restplus import Resource

from app.main.helpers.common_helper import UtilHelper

from ..util.dto import QueueDto
from ..service.queue_service import SampleQueue
from ..service.queue_singleton_service import SampleQueueIterator



api = QueueDto.api
_api_model = QueueDto.api_model
_SampleQueue = SampleQueue()

@api.route('/add')
class QueueAdd(Resource):
    @api.response(201, 'Data successfully received in redis.')
    @api.doc('receive a new data in redis')
    def post(self) -> dict:
        """
        Recieve and add data to redis Queue

        :returns:   Api reponse
        :rtype:     dict
        """
        data = request.json
        return _SampleQueue.save_data(data=data)


@api.route('/read')
class QueueAdd(Resource):
    @api.response(201, 'Data successfully read in redis.')
    @api.doc('reads datas in redis from head')
    def get(self) -> list:
        """
        get's all the data in redis Queue

        :returns:   Api reponse
        :rtype:     list
        """
        total_count = request.args.get('total_count', 1)
        return _SampleQueue.get_from_head(total_count)


@api.route('/singleton')
class QueueSingleto(Resource):
    @api.response(201, 'Data successfully read in redis via singleton iterator')
    @api.doc('reads datas in redis from head via singleton iterator')
    def get(self) -> list:
        """
        get's all the data in redis Queue via singleton iterator

        :returns:   Api reponse
        :rtype:     list
        """
        try:
            datas = []
            sample_queue_iterator = SampleQueueIterator(1)
            UtilHelper.show_module_path(SampleQueueIterator)
            total_count = request.args.get('total_count', 1)
            for item in sample_queue_iterator:
                print(item)
            return {'success': True, 'datas' : datas}, 201
        except Exception as e:
            return {'success': False, 'message' : str(e)}, 442
        finally:
            pass


@api.route('/flush')
class QueueAdd(Resource):
    @api.response(201, 'Data successfully flush in redis.')
    @api.doc('flush all datas in redis')
    def get(self) -> dict:
        """
        flush all data

        :returns:   Api reponse
        :rtype:     dict
        """
        return _SampleQueue.flushall()

