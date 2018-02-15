import xml.etree.ElementTree as ET

from .client import Client
from . import utils


class SubClientConfiguration(Client):
    """
    Alma provides a set of Web services for handling Configuration related
    information, enabling you to quickly and easily receive configuration details.
    These Web services can be used by external systems in order to get list of
    possible data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/conf
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/conf"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/conf"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/37088dc9-c685-4641-bc7f-60b5ca7cabed.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of api
        self.units = SubClientConfigurationUnits(self.cnxn_params)
        self.general = SubClientConfigurationGeneral(self.cnxn_params)
        self.jobs = SubClientConfigurationJobs(self.cnxn_params)
        self.sets = SubClientConfigurationSets(self.cnxn_params)


class SubClientConfigurationUnits(Client):
    """Handles the Organization Unit endpoints of Configurations API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()

    def get_libaries(self, library_id=None, q_params={}, raw=False):
        """Retrieve a list of libraries or a specific library

        Args:
            library_id (str): The code of the library (libraryCode).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of libraries or single library

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += '/libraries'
        if library_id:
            url += ("/" + str(library_id))

        response = self.fetch(url, args, raw=raw)
        return response

    def get_locations(self, library_id, location_id=None, q_params={}, raw=False):
        """Retrieve a list of locations for a library

        Args:
            library_id (str): The code of the library (libraryCode).
            location_id (str): Code for a specific location (locationCode).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of library locations.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += ('/libraries/' + str(library_id) + "/locations")
        if location_id:
            url += ("/" + str(location_id))

        response = self.fetch(url, args, raw=raw)
        return response

    def get_departments(self, q_params={}, raw=False):
        """Retrieve a list of configured departments

        Args:
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of departments.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += '/departments'

        response = self.fetch(url, args, raw=raw)
        return response


class SubClientConfigurationGeneral(Client):
    """Handles the General endpoints of Configurations API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()

    def get(self, library_id=None, q_params={}, raw=False):
        """Retrieve general configuration of the institution

        Args:
            library_id (str): The code of the library (libraryCode).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            General configuration of the institution
        """

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += "/general"

        response = self.fetch(url, args, raw=raw)
        return response

    def get_hours(self, library_id=None, q_params={}, raw=False):
        """Retrieve open hours as configured in Alma.
        Note that the library-hours do not necessarily reflect when the
        library doors are actually open, but rather start and end times that
        effect loan period.
        This API is limited to one month of days from 1 year ago to
        3 years ahead for a single request.

        Args:
            library_id (str): The code of the library (libraryCode).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of open hours

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']

        if library_id:
            url += '/libraries'
            url += ("/" + str(library_id))

        url += '/open-hours'

        response = self.fetch(url, args, raw=raw)
        return response

    def get_code_table(self, table_name, q_params={}, raw=False):
        """This API returns all rows defined for a code-table.

        The main usage of this API is for applications that use Alma APIs,
        and need to give the user a drop-down of valid values to choose from.

        See Alma documentation for code-table names.

        Args:
            table_name (str): Code table name. (codeTableName)
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Code-table rows

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += ('/code-tables/' + str(table_name))

        response = self.fetch(url, args, raw=raw)
        return response


class SubClientConfigurationJobs(Client):
    """Handles the Jobs endpoints of Configurations API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/jobs'
        self.cnxn_params['api_uri_full'] += '/jobs'

    def get(self, job_id=None, limit=10, offset=0, all_records=False,
            q_params={}, raw=False):
        """Retrieve a list of jobs that can be submitted or details for a given job.

        Args:
            job_id (str): Unique id of the job.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of jobs or a specific job

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']

        if job_id:
            url += ("/" + str(job_id))
        else:

            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.fetch(url, args, raw=raw)

        if job_id:
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
                    response['job'] += new_response['job']
                elif type(new_response) == ET.Element:
                    for row in list(new_response):
                        response.append(row)
                elif raw:
                    responses.append(new_response)

            if raw:
                return responses
        return response

    def get_instances(self, job_id, instance_id=None, limit=10, offset=0,
                      all_records=False, q_params={}, raw=False):
        """Retrieve all the job instances (runs) for a given job id, or specific instance.

        Args:
            job_id (str): Unique id of the job.
            instance_id (str): Unique id of the specific job instance.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of jobs or a specific job

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(job_id) + "/instances")

        if instance_id:
            url += ("/" + str(instance_id))
        else:

            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.fetch(url, args, raw=raw)

        if instance_id:
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
                    response['job_instance'] += new_response['job_instance']
                elif type(new_response) == ET.Element:
                    for row in list(new_response):
                        response.append(row)
                elif raw:
                    responses.append(new_response)

            if raw:
                return responses
        return response


class SubClientConfigurationSets(Client):
    """Handles the Sets endpoints of Configurations API
    A set is a collection of items, such as users or the results of a repository search.
    Sets may be used for publishing metadata in bulk, moving a group of records, or to run jobs.
    """

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/sets'
        self.cnxn_params['api_uri_full'] += '/sets'

    def get(self, set_id=None, content_type=None, set_type=None,
            query={}, limit=10, offset=0, all_records=False,
            q_params={}, raw=False):
        """Retrieve a list of sets or a single set.

        Args:
            set_id (str): A unique identifier of the set.
            content_type (str): Content type for filtering.
                Valid values are from the SetContentType code table.
            set_type (str):	Set type for filtering.
                Valid values are 'ITEMIZED' or 'LOGICAL'.
            query (dict): Search query. Searching for words in created_by or name
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of sets or a specific set.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if set_id:
            url += ("/" + str(set_id))
        else:
            # include paramets specific to user list
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)
            if content_type:
                args['content_type'] = str(content_type)
            if set_type:
                args['set_type'] = str(set_type)

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
        if set_id:
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
                    response['set'] += new_response['set']
                elif type(new_response) == ET.Element:
                    for row in list(new_response):
                        response.append(row)
                elif raw:
                    responses.append(new_response)

            if raw:
                return responses
        return response

    def get_members(self, set_id, limit=10, offset=0, all_records=False,
                    q_params={}, raw=False):
        """Retrieves members of a Set given a Set ID.

        Args:
            set_id (str): A unique identifier of the set.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of members for a specific set

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(set_id) + "/members")

        if int(limit) > 100:
            limit = 100
        elif int(limit) < 1:
            limit = 1
        else:
            limit = int(limit)
        args['limit'] = limit
        args['offset'] = int(offset)

        response = self.fetch(url, args, raw=raw)

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
                    response['member'] += new_response['member']
                elif type(new_response) == ET.Element:
                    for row in list(new_response):
                        response.append(row)
                elif raw:
                    responses.append(new_response)

            if raw:
                return responses
        return response
