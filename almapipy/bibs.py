from .client import Client
from . import utils


class SubClientBibs(Client):
    """
    Handles requests to bib endpoint.
    For more info: https://developers.exlibrisgroup.com/alma/apis/bibs
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to Bibs.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/bibs"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/bibs"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/af2fb69d-64f4-42bc-bb05-d8a0ae56936e.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of bib
        self.catalog = SubClientBibsCatalog(self.cnxn_params)
        self.collections = SubClientBibsCollections(self.cnxn_params)


class SubClientBibsCatalog(Client):
    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params

    def get(self, bib_ids, q_params={}, raw=False):
        """
        Returns Bib records from a list of Bib IDs submitted in a parameter.

        Args:
            bib_ids (list or str): list of bib Record IDs. len = 1-100.
                or string of one record id.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Returns a single or list of bib records.
            https://developers.exlibrisgroup.com/alma/apis/xsd/rest_bibs.xsd?tags=GET

        """
        url = self.cnxn_params['api_uri_full']

        # validate arguments
        if type(q_params) != dict:
            message = "q_params must be a dictionary."
            raise utils.ArgError(message)
        if type(bib_ids) != list and type(bib_ids) != str:
            message = "bib_ids must be a list of ids, or single string."
            raise utils.ArgError(message)

        # format arguments
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        # determine which endpoint to call.
        if type(bib_ids) == str:
            url += ('/' + bib_ids)
        else:
            args['mms_id'] = bib_ids

        if raw:
            return self.fetch(url, args, raw=True)
        else:
            return self.fetch(url, args)

    def get_holdings(self, bib_id, holding_id=None, q_params={}, raw=False):
        """Returns list of holding records or single holding record
            for a given bib record ID.

            If retrieving a single holding record with the holding_id param,
            it is returned as MARC XML format, so it is not recommended to
            use this service with JSON format.
            You can overide the json global setting
            by entering 'format':'xml' as item in q_params parameter.

        Args:
            bib_id (str): The bib ID (mms_id).
            holding_id (str): The Holding Record ID.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of holding records or single holding record
                for a given bib record ID.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += '/holdings'
        if holding_id:
            url += ('/' + str(holding_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        if raw:
            return self.fetch(url, args, raw=True)
        else:
            return self.fetch(url, args)

    def get_holding_items(self, bib_id, holding_id, item_id=None, q_params={}, raw=False):
        """Returns list of holding record items or a single item
            for a given holding record of a bib.
            Includes label printing information

        Args:
            bib_id (str): The bib ID (mms_id).
            holding_id (str): The Holding Record ID (holding_id).
            item_id (str): The holding item id (item_pid).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of holding record items or a single item
                for a given bib record ID.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += ('/holdings/' + str(holding_id)) + '/items'
        if item_id:
            url += ('/' + str(item_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        if raw:
            return self.fetch(url, args, raw=True)
        else:
            return self.fetch(url, args)

    def get_portfolios(self, bib_id, portfolio_id=None, q_params={}, raw=False):
        """Returns a list or single portfolio for a Bib.

            If retrieving a single holding record with the holding_id param,
            it is returned as MARC XML format, so it is not recommended to
            use this service with JSON format.
            You can overide the json global setting
            by entering 'format':'xml' as item in q_params parameter.

        Args:
            bib_id (str): The bib ID (mms_id).
            portfolio_id (str): The Electronic Portfolio ID.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Returns a list or single portfolio for a Bib.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += '/portfolios'
        if portfolio_id:
            url += ('/' + str(portfolio_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        if raw:
            return self.fetch(url, args, raw=True)
        else:
            return self.fetch(url, args)


class SubClientBibsCollections(Client):
    """Handles collections"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/collections'
        self.cnxn_params['api_uri_full'] += '/collections'

    def get(self, pid=None, q_params={}, raw=False):
        """Returns meta data about collections in libraries.
            If pid argument is used, will only return one collection.

        Args:
            pid (str): The collection ID.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            A list of collections or a collection for a given pid.

        """
        url = self.cnxn_params['api_uri_full']
        if pid:
            url += ("/" + str(pid))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        if raw:
            return self.fetch(url, args, raw=True)
        else:
            return self.fetch(url, args)

    def get_bibs(self, pid, q_params={}, raw=False):
        """Get bibs in a collection using pid.

        Args:
            pid (str): The collection ID.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            A a list of bibliographic titles in a given collection.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(pid))
        url += '/bibs'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        if raw:
            return self.fetch(url, args, raw=True)
        else:
            return self.fetch(url, args)
