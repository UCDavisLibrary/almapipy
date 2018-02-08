import xml.etree.ElementTree as ET

from .client import Client
from . import utils


class SubClientCourses(Client):
    """
    The Courses API allows access to courses and reading lists related information.
    These Web services can be used by external systems such as Courses Management
    Systems to retrieve or update courses and reading lists related data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/courses
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/courses"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/courses"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/25ede018-da5d-4780-8fda-a8e5d103faba.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']
        #self.cnxn_params['xml_ns']['report'] = 'urn:schemas-microsoft-com:xml-analysis:rowset'

        # Hook in subclients of api

    def get(self, course_id=None, query={}, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a courses list or a single course.

        Args:
            course_id (str): The identifier of a single course.
                Gets more detailed information.
            query (dict): Search query for filtering a course list. Optional.
                Searching for words from fields: [code, section, name, notes,
                instructors, searchable_ids, year, academic_department,
                all]. Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'code': 'ECN'} returns a list of econ classes
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): Offset of the results returned.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of courses or a specific course resource.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if course_id:
            url += ("/" + str(course_id))
        else:
            # include paramets specific to course list
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

            # add search query if specified in desired format
            if query:
                q_str = ""
                i = 0
                for field, filter_value in query.items():
                    if i > 0:
                        q_str += " AND "
                    q_str += (field + "~")
                    q_str += filter_value.replace(" ", "_")
                    i += 1
                args['q'] = q_str

        response = self.fetch(url, args, raw=raw)
        if course_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            if raw:
                responses = [response]
                response = response.json()
            args['offset'] = limit

            # get total record count of query
            if type(response) == dict:
                total_records = int(response['total_record_count'])
            elif type(response) == ET.Element:
                total_records = int(response.attrib['total_record_count'])
            else:
                total_records = limit

            records_retrieved = limit
            while True:
                if total_records <= records_retrieved:
                    break

                # make call and increment counter variables
                new_response = self.fetch(url, args, raw=raw)
                records_retrieved += limit
                args['offset'] += limit

                # append new records to initial response
                if type(new_response) == dict:
                    total_records = response['total_record_count']
                    response['course'] += new_response['course']
                elif type(new_response) == ET.Element:
                    for row in list(new_response):
                        response.append(row)
                elif raw:
                    responses.append(new_response)

            if raw:
                return responses
        return response
