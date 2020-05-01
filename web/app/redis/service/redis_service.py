__author__ = "Todd Lewellen"
"""
ENHANCED BY navagis team <josel.mariano@navagis.com>
ORIGINAL SCRIPT FROM https://gist.github.com/lewellent/d5b471bfd677c7121244
"""

"""
The MIT License (MIT)

Copyright (c) 2014 Todd Lewellen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Generic
import time
import datetime

# Library
import redis


class SetQueue(object):
    """
    A Redis-backed Set Queue with FIFO ordering.  Useful for queueing up
    recurring tasks and ensuring that a task is only queued once at any given
    time.  If all tasks are equally important, yet certain tasks are produced
    (enqueued) more than others, this FIFO Set Queue may be a good solution.

    Redis transactions are used to help ensure atomicity.

    This system relies on the assumption that the system times of the tasks
    producers are synced.

    Initial inspiration:
    http://www.rediscookbook.org/implement_a_fifo_queue.html
    """

    def __init__(self, host="localhost", port=6379, queue_name=None):
        """
        Constructs a new instance.

        :param      host:        The redis host
        :type       host:        string
        :param      port:        The redis port
        :type       port:        number
        :param      queue_name:  The queue name
        :type       queue_name:  string
        """

        """
        Redis instance connection
        """
        self.r = redis.Redis(host=host, port=port,
                             charset="utf-8", decode_responses=True)
        print(redis.__file__)
        """
        Redis queue name
        """
        _id = queue_name or self.r.incr("queue_space")
        self.queue = "queue:{}".format(_id)

    def get_mili_timestamp(self):
        """
        Gets the mili timestamp.

        :returns:   The mili timestamp.
        :rtype:     string
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def push(self, element):
        """Push an element to the tail of the queue"""
        self._zaddnx(element)

    def pop(self):
        """Pop an element from the head of the queue"""
        return self._zpop()

    def get_all(self, total_limit = 10) -> list:
        """
        Get a range of elements from the head of the queue with default limit of
        10

        :param      total_limit:  The total limit
        :type       total_limit:  number

        :returns:   All.
        :rtype:     list
        """
        return self._zrange(total_limit)

    def _zaddnx(self, element):
        """
        Push an element to the tail of the queue

        :param      element:  The element
        :type       element:  None
        """
        pipe = self.r.pipeline()
        while 1:
            try:
                pipe.watch(self.queue)
                score = pipe.zscore(self.queue, element)
                if score is None:
                    t_score = time.time()
                    pipe.multi()
                    pipe.zadd(self.queue, {element: t_score})
                    pipe.execute()
                break
            except redis.WatchError:
                continue

    def _zpop(self):
        """
        Pop an element to the head of the queue

        :param      element:  The element
        :type       element:  string
        """
        pipe = self.r.pipeline()
        while 1:
            data = None
            try:
                pipe.watch(self.queue)
                rs = pipe.zrange(self.queue, 0, 0)
                if len(rs) > 0:
                    element = rs[0]
                    pipe.multi()
                    pipe.zrem(self.queue, element)
                    pipe.execute()
                    data = element
                else:
                    data = None
                return data
                break
            except (redis.WatchError, IndexError):
                continue

    def _zrange(self, total_limit = 10):
        """
        Get a range of elements from the head of the queue with default limit of
        10

        :param      total_limit:  The total limit
        :type       total_limit:  number
        :param      element:  The element
        :type       element:  list

        :returns:   { description_of_the_return_value }
        :rtype:     { return_type_description }
        """
        pipe = self.r.pipeline()
        while 1:
            data = []
            try:
                pipe.watch(self.queue)
                rs = pipe.zrange(self.queue, 0, total_limit)
                if len(rs) <= 0:
                    print("REDIS : SetQueue - No elements left!")
                return rs
                break
            except (redis.WatchError, IndexError):
                continue