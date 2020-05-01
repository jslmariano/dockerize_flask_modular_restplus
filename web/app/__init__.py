from flask_restplus import Api
from flask import Blueprint

# Main
from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

# Work Order
from .workorder.controller.receiver_controller import api as wo_receiver_ns
from .redis.controller.queue_controller import api as queue_pipe_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(wo_receiver_ns, path='/workorder/receiver')
api.add_namespace(queue_pipe_ns, path='/redis/queue')