from __future__ import annotations
import argparse

from app.main.service.singleton_service import SingletonMeta
from app.redis.service.redis_service import SetQueue

class SampleQueueIterator(metaclass=SingletonMeta):
    """
    Sample Queue Iterator

    An items iterator for redis pipeline that implements singleton
    """

    def __init__(self, total):
        """
        Constructs a new instance.

        :param      total:  The total
        :type       total:  number
        """
        super(SampleQueueIterator, self).__init__()
        self.check_positive(total)
        # Redis instance for sapel queue
        self.queue_name = "sample"
        self.queue = SetQueue(host="redis", queue_name=self.queue_name)
        self.pipe = self.queue.r.pipeline()
        # iterators properties
        self.__start = 0
        self.__total = total
        self.__current_element = None
        self.__current_cursor = 0
        self.max = 10

    def check_positive(self, value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"Can't instantiate {str(self)}"
                                             f" with {value}, an invalid "
                                             "positive int value")
        return ivalue

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        self.pipe.watch(self.queue_name)

        # Stop iterator if meets ends
        if self.__current_cursor >= self.__total:
             raise StopIteration

        try:
            rs = self.pipe.zrange(self.queue_name, 0, self.__current_cursor)
            self.__current_cursor =+ 1
            # Stop itrator if there are no more left
            if len(rs) <= 0:
                self.__current_element = None
                raise StopIteration
            self.__current_element = rs[0]
            return rs[0]
        except Exception as e:
            raise StopIteration

    def remove_element(self, element) -> SampleQueueIterator:
        """
        Removes an element.

        :param      element:  The element
        :type       element:  { type_description }
        """
        return self

    def remove_all(self) -> SampleQueueIterator:
        """
        Removes all data within the range.

        :returns:   The sample queue iterator.
        :rtype:     SampleQueueIterator
        """
        return self