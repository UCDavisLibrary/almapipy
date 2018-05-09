"""
Common Client for interacting with Alma API
"""

import json
import xml.etree.ElementTree as ET

import requests

from . import utils


class Client(object):
    """
    Reads responses from Alma API and handles response.
    """

    def __init__(self, cnxn_params={}):
        # instantiate dictionary for storing alma api connection parameters
        self.cnxn_params = cnxn_params

    def create(self, url, data, args, object_type, raw=False):
        """
        Uses requests library to make Exlibris API Post call.

        Args:
            url (str): Exlibris API endpoint url.
            data (dict): Data to be posted.
            args (dict): Query string parameters for API call.
            object_type (str): Type of object to be posted (see alma docs)
            raw (bool): If true, returns raw response.

        Returns:
            JSON-esque, xml, or raw response.
        """
        print(url)

        # Determine format of data to be posted according to order of importance:
        # 1) Local declaration, 2) dtype of data parameter, 3) global setting.
        headers = {}
        if 'format' not in args.keys():
            if type(data) == ET or type(data) == ET.Element:
                content_type = 'xml'
            elif type(data) == dict:
                content_type = 'json'
            else:
                content_type = self.cnxn_params['format']
            args['format'] = self.cnxn_params['format']
        else:
            content_type = args['format']

        # Declare data type in header, convert to string if necessary.
        if content_type == 'json':
            headers['content-type'] = 'application/json'
            if type(data) != str:
                data = json.dumps(data)
        elif content_type == 'xml':
            headers['content-type'] = 'application/xml'
            if type(data) == ET or type(data) == ET.Element:
                data = ET.tostring(data, encoding='unicode')
            elif type(data) != str:
                message = "XML payload must be either string or ElementTree."
                raise utils.ArgError(message)
        else:
            message = "Post content type must be either 'json' or 'xml'"
            raise utils.ArgError(message)

        # Send request and parse response
        response = requests.post(url, data=data, params=args, headers=headers)
        if raw:
            return response
        content = self.__parse_response__(response)

        return content

    def read(self, url, args, raw=False):
        """
        Uses requests library to make Exlibris API Get call.
        Returns data of type specified during init of base class.

        Args:
            url (str): Exlibris API endpoint url.
            args (dict): Query string parameters for API call.
            raw (bool): If true, returns raw response.

        Returns:
            JSON-esque, xml, or raw response.
        """
        # print(url)

        # handle data format. Allow for overriding of global setting.
        data_format = self.cnxn_params['format']
        if 'format' not in args.keys():
            args['format'] = data_format
        data_format = args['format']

        # Send request.
        response = requests.get(url, params=args)
        if raw:
            return response

        # Parse content
        content = self.__parse_response__(response)

        return content

    def __format_query__(self, query):
        """Converts dictionary of brief search query to a formated string.
        https://developers.exlibrisgroup.com/blog/How-we-re-building-APIs-at-Ex-Libris#BriefSearch

        Args:
            query: dictionary of brief search query.
                Format - {'field': 'value', 'field2', 'value2'}.
        Returns:
            String of query.
        """
        q_str = ""
        i = 0
        if type(query) != 'dict':
            message = "Brief search query must be a dictionary."
        for field, filter_value in query.items():
            field = str(field)
            filter_value = str(filter_value)
            if i > 0:
                q_str += " AND "
            q_str += (field + "~")
            q_str += filter_value.replace(" ", "_")
            i += 1

        return q_str

    def __read_all__(self, url, args, raw, response, data_key, max_limit=100):
        """Makes multiple API calls until all records for a query are retrieved.
            Called by the 'all_records' parameter.

        Args:
            url (str): Exlibris API endpoint url.
            args (dict): Query string parameters for API call.
            raw (bool): If true, returns raw response.
            response (xml, raw, or json): First API call.
            data_key (str): Dictionary key for accessing data.
            max_limit (int): Max number of records allowed to be retrieved in a single call.
                Overrides limit parameter. Reduces the number of API calls needed to retrieve data.

        Returns:
            response with remainder of data appended.
            """
        # raw will return a list of responses
        if raw:
            responses = [response]
            response = response.json()

        args['offset'] = args['limit']
        limit = args['limit']

        # get total record count of query
        if type(response) == dict:
            total_records = int(response['total_record_count'])
        elif type(response) == ET.Element:
            total_records = int(response.attrib['total_record_count'])
        else:
            total_records = limit

        # set new retrieval limit
        records_retrieved = limit
        args['limit'] = max_limit
        limit = max_limit

        while True:
            if total_records <= records_retrieved:
                break

            # make call and increment counter variables
            new_response = self.read(url, args, raw=raw)
            records_retrieved += limit
            args['offset'] += limit

            # append new records to initial response
            if type(new_response) == dict:
                response[data_key] += new_response[data_key]
            elif type(new_response) == ET.Element:
                for row in list(new_response):
                    response.append(row)
            elif raw:
                responses.append(new_response)

        if raw:
            response = responses

        return response

    def __parse_response__(self, response):
        """Parses alma response depending on content type.

        Args:
            response: requests object from Alma.

        Returns:
            Content of response in format specified in header.
        """
        status = response.status_code
        url = response.url
        try:
            response_type = response.headers['Content-Type']
            if ";" in response_type:
                response_type, charset = response_type.split(";")
        except:
            message = 'Error ' + str(status) + response.text
            raise utils.AlmaError(message, status, url)

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
                    message += " See Alma documentation for more information."
                except:
                    message = 'Error ' + str(status) + " - " + str(content)
                raise utils.AlmaError(message, status, url)

        # decode response if json.
        elif response_type == 'application/json':
            content = response.json()

            # Received response from ex libris, but error retrieving data.
            if str(status)[0] in ['4', '5']:
                try:
                    if 'web_service_result' in content.keys():
                        first_error = content['web_service_result']['errorList']['error'][0]
                    else:
                        first_error = content['errorList']['error'][0]
                    message = first_error['errorCode']
                    message += " - "
                    message += first_error['errorMessage']
                    if 'trackingID' in first_error.keys():
                        message += "TrackingID: " + message['trackingID']
                    message += " See Alma documentation for more information."
                except:
                    message = 'Error ' + str(status) + " - " + str(content)
                raise utils.AlmaError(message, status, url)

        else:
            content = response

            if str(status)[0] in ['4', '5']:
                message = str(status) + " - "
                message += str(content.text)
                raise utils.AlmaError(message, status, url)
        return content
