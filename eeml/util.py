"""
Some utility functions, not for public use
"""

try:
    from lxml import etree
except ImportError: # If lxml is not there try python standard lib
    from xml.etree import ElementTree as etree

from eeml.namespace import EEML_NAMESPACE, NSMAP

def _elem(name):
    """
    Create an element in the EEML namespace
    """
    return etree.Element("{{{}}}{}".format(EEML_NAMESPACE, name), nsmap=NSMAP)


def _addE(env, attr, name, call=lambda x: x):
    """
    Helper method to add child if not None
    """
    if attr is not None:
        tmp = _elem(name)
        tmp.text = call(attr)
        env.append(tmp)


def _addA(env, attr, name, call=lambda x: x):
    """
    Helper method to add attribute if not None
    """
    if attr is not None:
        env.attrib[name] = call(attr)


def _assertPosInt(val, name, required=False):
    """
    Check if val is positive integer. If val is None ValueError is raised
    if required is True
    """
    if isinstance(val, (int, long)):
        if val < 0:
            raise ValueError("Positive integer is required as {}, got {}"
                             .format(name, val))
    elif val is not None:
        raise ValueError("Integer value is required as {}, got {}"
                         .format(name, type(val)))
    elif required:
        raise ValueError("{} is required, got {}".format(name, val))
