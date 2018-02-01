"""
Common Client for interacting with Alma API
"""

import json
import xml.etree.ElementTree as ET

import requests

from . import utils


class Client(object):
    """
    Fetches responses from Alma API and handles response.
    """

    def __init__(self, cnxn_params={}):
        # instantiate dictionary for storing alma api connection parameters
        self.cnxn_params = cnxn_params

    def fetch(self, url, args, raw=False):
        """
        Uses requests library to makes Exlibris API call.
        Parses XML into python.

        Args:
            url (str): Exlibris API endpoint url.
            args (dict): Query string parameters for API call.
            raw (bool): If true, returns raw response.

        Returns:
            JSON-esque or raw response.
        """
        print(url)

        # handle data format. Allow for overriding of global setting.
        data_format = self.cnxn_params['format']
        if 'format' not in args.keys():
            args['format'] = data_format
        data_format = args['format']

        # Send request.
        response = requests.get(url, params=args)
        if raw:
            return response

        # Get meta data from headers.
        response_type = response.headers['Content-Type']
        response_type, charset = response_type.split(";")
        status = response.status_code

        # decode response if xml.
        if response_type == 'application/xml':
            xml_ns = self.cnxn_params['xml_ns']  # xml namespace
            content = ET.fromstring(response.text)

            # Received response from ex libris, but error retrieving data.
            if str(status)[0] in ['4', '5']:
                try:
                    first_error = content.find("header:errorList", xml_ns)[0]
                    message = first_error.find("header:errorCode", xml_ns).text
                    message += " - "
                    message += first_error.find("header:errorMessage", xml_ns).text
                    message += ". See Alma documentation for more information."
                except:
                    message = str(status) + " - Unknown Error"
                raise utils.AlmaError(message, status, url)

        # decode response if json.
        elif response_type == 'application/json':
            content = response.json()

            # Received response from ex libris, but error retrieving data.
            if str(status)[0] in ['4', '5']:
                try:
                    first_error = content['errorList']['error'][0]
                    message = first_error['errorCode']
                    message += " - "
                    message += first_error['errorMessage']
                    message += ". See Alma documentation for more information."
                except:
                    message = str(status) + " - Unknown Error"
                raise utils.AlmaError(message, status, url)

        else:
            content = response

            if str(status)[0] in ['4', '5']:
                message = str(status) + " - "
                message += str(content.text)
                raise utils.AlmaError(message, status, url)

        return content
