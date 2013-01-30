"""
XML namespace definitions
"""

EEML_SCHEMA_VERSION = '0.5.1'
EEML_NAMESPACE = 'http://www.eeml.org/xsd/{}'.format(EEML_SCHEMA_VERSION)
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
SCHEMA_LOCATION = ('{{{}}}schemaLocation'.format(XSI_NAMESPACE),
                   EEML_NAMESPACE +
                   ' http://www.eeml.org/xsd/{0}/{0}.xsd'
                   .format(EEML_SCHEMA_VERSION))
NSMAP = {None: EEML_NAMESPACE,
         'xsi': XSI_NAMESPACE}

