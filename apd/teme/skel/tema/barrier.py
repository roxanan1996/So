""" implementation of a reentrant barrier
    from lab3
"""
from threading import Condition

class ReusableBarrierCond(object):
    """ Bariera reentranta, implementata folosind o variabila conditie """

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count_threads = self.num_threads
        self.cond = Condition()

    def wait(self):
        """ wait implemenation """
        self.cond.acquire()
        self.count_threads -= 1
        if self.count_threads == 0:
            self.cond.notify_all()
            self.count_threads = self.num_threads
        else:
            self.cond.wait()
        self.cond.release()
