from threading import Event

""" Directory for ids and corresponding hostnames and ports. """
""" Every entry in the directory is a tuple of (hostname, port) against the id. """

dir_proposers = { 0: ('localhost', 5000), 1: ('localhost', 5001), 2: ('localhost', 5002) }
dir_acceptors = { 0: ('localhost', 6000), 1: ('localhost', 6001), 2: ('localhost', 6002) }
dir_learners = { 0: ('localhost', 7000), 1: ('localhost', 7001), 2: ('localhost', 7002) }

dir_net = {0: ('localhost', 5000), 1: ('localhost', 5001), 2: ('localhost', 5002), 3: ('localhost', 6000), 4: ('localhost', 6001), 5: ('localhost', 6002), 6: ('localhost', 7000), 7: ('localhost', 7001), 8: ('localhost', 7002)}


""" Timer """

# Class Definitions
class Sleep(object):
    def __init__(self, seconds, immediate=True):
        self.seconds = seconds
        self.event = Event()
        if immediate:
            self.sleep()

    def sleep(self, seconds=None):
        if seconds is None:
            seconds = self.seconds
        self.event.clear()
        self.event.wait(timeout=seconds)

    def wake(self):
        self.event.set()
