from .client import Client
from . import utils


class SubClientPrimoSearch(Client):
    """
    Handles requests to bib endpoint.
    For more info: https://developers.exlibrisgroup.com/alma/apis/bibs
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to Bibs.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/primo/v1/search"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/primo/apis/search"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/f5643222-bb88-4f3d-b2d6-5029e527c515.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

    def get(self, query, view_id, tab="default_tab", scope="everything_scope", q_params={}, raw=False):
        """Returns a list of results based on the specified search query

        Args:
            query (string): Query string you want to preform a search.
            view_id (string): The view ID.
            tab (str): Name of the tab
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Returns a list or single portfolio for a Bib.
        """
        url = self.cnxn_params['api_uri_full']

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['vid'] = str(view_id)
        args['tab'] = str(tab)
        args['scope'] = str(scope)
        args['q'] = query

        return self.read(url, args, raw=raw)
