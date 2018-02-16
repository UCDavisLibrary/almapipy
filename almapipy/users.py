from .client import Client
from . import utils


class SubClientUsers(Client):
    """
    Alma provides a set of Web services for handling user information,
    enabling you to quickly and easily manipulate user details.
    These Web services can be used by external systems
    such as student information systems (SIS)—to retrieve or update user data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/users
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/users"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/users"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/0aa8d36f-53d6-48ff-8996-485b90b103e4.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of api
        self.loans = SubClientUsersLoans(self.cnxn_params)
        self.requests = SubClientUsersRequests(self.cnxn_params)
        self.fees = SubClientUsersFees(self.cnxn_params)
        self.deposits = SubClientUsersDeposits(self.cnxn_params)

    def get(self, user_id=None, query={}, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a user list or a single user.

        Args:
            user_id (str): 	A unique identifier for the user.
                Gets more detailed information.
            query (dict): Search query for filtering a user list. Optional.
                Searching for words from fields: [primary_id, first_name,
                last_name, middle_name, email, job_category, identifiers,
                general_info and ALL.].
                Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'first_name': 'Sterling', 'last_name': 'Archer'}
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of user or a specific user's details.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if user_id:
            url += ("/" + str(user_id))
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

            # add search query if specified in desired format
            if query:
                args['q'] = self.__format_query__(query)

        response = self.read(url, args, raw=raw)
        if user_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='user')
        return response


class SubClientUsersLoans(Client):
    """Handles the Loans endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, user_id, loan_id=None, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of loans for a user.

        Args:
            user_id (str): 	A unique identifier for the user.
            loan_id (str): 	A unique identifier for the loan.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of loans or a specific loan for a given user.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += (str(user_id) + "/loans")

        if loan_id:
            url += ('/' + str(loan_id))
        else:
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.read(url, args, raw=raw)
        if loan_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='item_loan')
        return response


class SubClientUsersRequests(Client):
    """Handles the Requests endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, user_id, request_id=None, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of requests for a user.

        Args:
            user_id (str): 	A unique identifier for the user.
            request_id (str): 	A unique identifier for the request.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of requests or a specific request for a given user.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += (str(user_id) + "/requests")

        if request_id:
            url += ('/' + str(request_id))
        else:
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.read(url, args, raw=raw)
        if request_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='user_request')
        return response


class SubClientUsersFees(Client):
    """Handles the Fines and Fees endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, user_id, fee_id=None, q_params={}, raw=False):
        """Retrieve a list of fines and fees for a user.

        Args:
            user_id (str): 	A unique identifier for the user.
            fee_id (str): 	A unique identifier for the fee.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of fines/fees or a specific fine/fee for a given user.

        """
        url = self.cnxn_params['api_uri_full']
        url += (str(user_id))
        url += '/fees'
        if fee_id:
            url += ('/' + str(fee_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)


class SubClientUsersDeposits(Client):
    """Handles the Deposits endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, user_id, deposit_id=None, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of deposits for a user.

        Args:
            user_id (str): 	A unique identifier for the user.
            deposit_id (str): A unique identifier for the deposit.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of deposits or a specific deposit for a given user.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += (str(user_id) + "/deposits")

        if deposit_id:
            url += ('/' + str(deposit_id))
        else:
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.read(url, args, raw=raw)
        if deposit_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='user_deposit')
        return response
