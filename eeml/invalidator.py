"""
Don't validate any input
"""


class Invalidator(object):
    """
    Doesn't do much
    """

    def environment(self, env):
        pass

    def location(self, loc):
        pass

    def data(self, data):
        pass

    def datapoints(self, datapoints):
        pass

Validator = Invalidator
