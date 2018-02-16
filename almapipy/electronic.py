from .client import Client
from . import utils


class SubClientElectronic(Client):
    """
    Alma provides a set of Web services for handling electronic information,
    enabling you to quickly and easily manipulate electronic details.
    These Web services can be used by external systems in order to retrieve or
    update electronic data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/electronic
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/electronic"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/electronic"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/e7cf39e9-adce-4be1-aeb9-a31f452960da.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of api
        self.collections = SubClientElectronicCollections(self.cnxn_params)
        self.services = SubClientElectronicServices(self.cnxn_params)
        self.portfolios = SubClientElectronicPortfolios(self.cnxn_params)


class SubClientElectronicCollections(Client):
    """Handles the e-collections endpoints of Electronic API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/e-collections'
        self.cnxn_params['api_uri_full'] += '/e-collections'

    def get(self, collection_id=None, query={}, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of electronic collections.

        Args:
            collection_id (str): 	Unique ID of the electronic collection.
            query (dict): Search query for filtering a course list. Optional.
                Searching for words from fields: [interface_name, keywords,
                name, po_line_id]. Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of electronic collections or specific collection.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if collection_id:
            url += ("/" + str(collection_id))
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
                args['q'] = self.__format_query__(query)

        response = self.read(url, args, raw=raw)
        if collection_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='electronic_collection')
        return response


class SubClientElectronicServices(Client):
    """Handles the e-services endpoints of Electronic API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/e-collections/'
        self.cnxn_params['api_uri_full'] += '/e-collections/'

    def get(self, collection_id, service_id=None, q_params={}, raw=False):
        """Returns a list of electronic services for a given electronic collection.

        Args:
            collection_id (str): Unique ID of the electronic collection.
            service_id (str): Unique ID of the electronic service.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of electronic services for a given electronic collection
                or a specific e-service.
        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += str(collection_id)
        url += '/e-services'
        if service_id:
            url += ('/' + str(service_id))

        return self.read(url, args, raw=raw)


class SubClientElectronicPortfolios(Client):
    """Handles the e-services endpoints of Electronic API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/e-collections/'
        self.cnxn_params['api_uri_full'] += '/e-collections/'

    def get(self, collection_id, service_id, portfolio_id=None, q_params={}, raw=False):
        """Returns a list of portfolios for an electronic services for a given electronic collection.

        Args:
            collection_id (str): Unique ID of the electronic collection.
            service_id (str): Unique ID of the electronic service.
            portfolio_id (str): Unique ID of the portfolio.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of portfolios for an electronic services for a given electronic collection
                or a specific portfolio.
        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += str(collection_id)
        url += '/e-services'
        url += ('/' + str(service_id))
        url += "/portfolios"
        if portfolio_id:
            url += ('/' + str(portfolio_id))
        return self.read(url, args, raw=raw)
