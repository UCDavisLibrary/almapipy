from .client import Client
from . import utils


class SubClientTaskList(Client):
    """
    Alma provides a set of Web services for handling task lists information,
    enabling you to quickly and easily manipulate their details.
    These Web services can be used by external systems.
    For more info: https://developers.exlibrisgroup.com/alma/apis/taskslists
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/task-lists"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/taskslists"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/d48a1a58-d90c-4eb2-b69f-c17f7a016fd3.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of api
        self.resources = SubClientTaskListResources(self.cnxn_params)
        self.lending = SubClientTaskListLending(self.cnxn_params)


class SubClientTaskListResources(Client):
    """Handles the requested resources endpoints of Task List API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/requested-resources'
        self.cnxn_params['api_uri_full'] += '/requested-resources'

    def get(self, library_id, circ_desk, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of requested resources to be picked from the shelf in Alma
            for a specific library/circ_desk.

        Args:
            library_id (str): The library of the given circulation desk or department where the resources are located.
                Use conf.units.get_libraries() to retrieve valid arguments.
            circ_desk (str): The circulation desk where the action is being performed.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of requested resources.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']

        if int(limit) > 100:
            limit = 100
        elif int(limit) < 1:
            limit = 1
        else:
            limit = int(limit)
        args['limit'] = limit
        args['offset'] = int(offset)
        args['library'] = str(library_id)
        args['circ_desk'] = str(circ_desk)

        response = self.read(url, args, raw=raw)

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args,
                                         raw=raw, response=response,
                                         data_key='requested_resource')
        return response


class SubClientTaskListLending(Client):
    """Handles the requested resources endpoints of Task List API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/rs/lending-requests'
        self.cnxn_params['api_uri_full'] += '/rs/lending-requests'

    def get(self, library_id, q_params={}, raw=False):
        """Retrieve list of lending requests in Alma.

        Args:
            library_id (str): The library of the given circulation desk or department where the resources are located.
                Use conf.units.get_libraries() to retrieve valid arguments.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of lending requests.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['library'] = str(library_id)

        url = self.cnxn_params['api_uri_full']

        response = self.read(url, args, raw=raw)

        return response
