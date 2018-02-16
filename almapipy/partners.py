from .client import Client
from . import utils


class SubClientPartners(Client):
    """
    Alma provides a set of Web services for handling Resource Sharing Partner
    information, enabling you to quickly and easily manipulate partner details.
    These Web services can be used by external systems to retrieve or update
    partner data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/partners
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/partners"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/partners"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/8883ef41-c3b8-4792-9ff8-cb6b729d6e07.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of api
        self.lending_requests = SubClientPartnersLending(self.cnxn_params)

    def get(self, partner_id=None, limit=10, offset=0, all_records=False,
            q_params={}, raw=False):
        """Retrieves a list of Resource Sharing Partners or specific partner.

        Args:
            partner_id (str): The code of the Resource Sharing Partner (partner_code).
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of partners or specific partner

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if partner_id:
            url += ("/" + str(partner_id))

        if int(limit) > 100:
            limit = 100
        elif int(limit) < 1:
            limit = 1
        else:
            limit = int(limit)
        args['limit'] = limit
        args['offset'] = int(offset)

        response = self.read(url, args, raw=raw)

        if partner_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='partner')
        return response


class SubClientPartnersLending(Client):
    """Handles the Lending Request endpoints of Resource Sharing Partners API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()

    def get(self, partner_id, request_id, q_params={}, raw=False):
        """Retrieve a lending request from a specific partner.

        Args:
            partner_id (str): The code of the Resource Sharing Partner (partner_code).
            request_id (str): The ID of the requested lending request.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Lending request from a specific partner.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(partner_id) + "/lending-requests")
        url += ("/" + str(request_id))

        response = self.read(url, args, raw=raw)
        return response
