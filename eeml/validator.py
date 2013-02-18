"""
Here are the validators
"""

from datetime import datetime

from eeml.unit import Unit
from eeml.util import _assertPosInt

import logging

class Version051(object):
    """
    Validate constructors by version 0.5.1 specification
    """

    def environment(self, env):
        status = env._status
        id_ = env._id
        private = env._private
        
        if status is not None and status not in ['frozen', 'live']:
            raise ValueError("status must be either 'frozen' or 'live', "
                             "got {}".format(status))
        _assertPosInt(id_, 'id', False)
        if private is not None and not isinstance(private, bool):
            raise ValueError("private is expected to be bool, got {}"
                             .format(type(private)))

    def location(self, loc):
        exposure = loc._exposure
        domain = loc._domain
        disposition = loc._disposition
        # TODO validate lat and lon

        if exposure is not None and exposure not in ['indoor', 'outdoor']:
            raise ValueError("exposure must be 'indoor' or 'outdoor', got '{}'"
                             .format(exposure))

        if domain not in ['physical', 'virtual']:
            raise ValueError("domain is required, must be 'physical' or 'virtual', got '{}'"
                             .format(domain))

        if disposition is not None and disposition not in ['fixed', 'mobile']:
            raise ValueError("disposition must be 'fixed' or 'mobile', got '{}'"
                             .format(disposition))

    def data(self, data):
        unit = data._unit
        at = data._at
        id_ = data._id

        _assertPosInt(id_, 'id', True)
        if unit is not None and not isinstance(unit, Unit):
            raise ValueError("unit must be an instance of Unit, got {}"
                             .format(type(unit)))
        if at is not None and not isinstance(at, datetime):
            raise ValueError("at must be an instance of datetime.datetime, "
                             "got {}".format(type(at)))

    def datapoints(self, datapoints):
        id_ = datapoints._id

        _assertPosInt(id_, 'id', True)

Validator = Version051
