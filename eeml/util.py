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


def _addE(env, attr, name):
    """
    Helper method to add child if not None
    """
    if attr is not None:
        tmp = _elem(name)
        tmp.text = str(attr)
        env.append(tmp)

def _addA(env, attr, name):
    """
    Helper method to add attribute if not None
    """
    if attr is not None:
        env.attrib[name] = str(attr)

