from __future__ import annotations
import json

from app.main.service.abstract_service import AbstractService
from app.redis.service.redis_service import SetQueue


class SampleQueue(AbstractService):
    """docstring for SampleQueue"""

    def __init__(self):
        super(SampleQueue, self).__init__()
        self.queue = SetQueue(host="redis", queue_name="sample")

    def save_data(self, data : Any) -> Response:
        """
        Saves a data.

        :param      data:  The data
        :type       data:  Any

        :returns:   Response message and status
        :rtype:     Response
        """

        try:
            self.queue.push(str(json.dumps(data)).encode('utf8'))
        except Exception as e:
            raise e
            return self.return_fail("Failed inserting data to redis : "
                                    f"{str(e)}")
        finally:
            return self.return_created("Sucesfully saved to redis pipeline")

    def get_from_head(self, total_count = 1) -> list:
        """
        Gets the data in redis pipeline from head.

        :param      total_count:  The total count
        :type       total_count:  number

        :returns:   The list datas from head.
        :rtype:     list
        """
        return self.queue.get_all(total_count)

    def flushall(self) -> Response:
        """
        Flash all object in redis pipeline

        :returns:   Response message and status
        :rtype:     Response
        """

        self.queue.r.flushall()
        return self.return_ok("Sucesfully flushed all data in redis pipeline")
