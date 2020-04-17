from __future__ import annotations
import aenum
from http import HTTPStatus
import pprint

class AbstractService(object):
    """docstring for AbstractService"""

    def return_fail(self, message : String = "") -> dict:
        return {
            'status' : 'fail',
            'message' : message,
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    def return_created(self, message : String, **kwargs) -> dict:
        response_object = {
            'status' : 'success',
            'message' : message,
        }
        response_object.update(kwargs)
        return response_object, HTTPStatus.CREATED

    def return_ok(self, message : String, **kwargs) -> dict:
        response_object = {
            'status' : 'success',
            'message' : message,
        }
        response_object.update(kwargs)
        return response_object, HTTPStatus.OK