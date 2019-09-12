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
        self.loans = SubClientBibsLoans(self.cnxn_params)
        self.requests = SubClientBibsRequests(self.cnxn_params)
        self.representations = SubClientBibsRepresentations(self.cnxn_params)
        self.linked_data = SubClientBibsLinkedData(self.cnxn_params)


class SubClientBibsCatalog(Client):
    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params

    def get(self, bib_ids, expand=None, q_params={}, raw=False):
        """
        Returns Bib records from a list of Bib IDs submitted in a parameter.

        Args:
            bib_ids (list or str): list of bib Record IDs. len = 1-100.
                or string of one record id.
            expand (str): provides additional information:
                p_avail - Expand physical inventory information.
                e_avail - Expand electronic inventory information.
                d_avail - Expand digital inventory information.
                To use more than one, use a comma separator.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Returns a single or list of bib records.
            https://developers.exlibrisgroup.com/alma/apis/xsd/rest_bibs.xsd?tags=GET

        """
        url = self.cnxn_params['api_uri_full']

        # validate arguments
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
            args['mms_id'] = ",".join(bib_ids)

        if expand:
            args['expand'] = expand

        return self.read(url, args, raw=raw)

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

        return self.read(url, args, raw=raw)

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

        return self.read(url, args, raw=raw)

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

        return self.read(url, args, raw=raw)

    def post(self, data, from_nz_mms_id=None, normalization=None, validate=False,
             q_params={}, raw=False):
        """Creates a new Bib record or local record for a NZ record.

        Args:
            data (xml/str): This method takes a Bib object.
                When creating linked record send an empty Bib object: <bib/>
                Note: JSON is not supported for this API.
            from_nz_mms_id (str): The MMS_ID of the Network-Zone record.
                Leave empty when creating a regular local record.
            normalization (str): The id of the normalization profile to run.
            validate (bool): Boolean flag for indicating whether to validate the record.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Bib object created.

        """
        url = self.cnxn_params['api_uri_full']
        object_type = 'bib'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['format'] = 'xml'

        if from_nz_mms_id:
            args['from_nz_mms_id'] = from_nz_mms_id
        if normalization:
            args['normalization'] = normalization
        if validate:
            args['validate'] = validate

        response = self.create(url, data, args, object_type, raw=raw)

        return response

    def post_holding(self, data, bib_id, q_params={}, raw=False):
        """Creates a a new holding record for a Bib record.

        Args:
            data (xml/str): This method takes a Holding object.
                Note: JSON is not supported for this API.
            bib_id (str): The bib ID (mms_id).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Holding object created.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += '/holdings'
        object_type = 'holding'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['format'] = 'xml'

        response = self.create(url, data, args, object_type, raw=raw)

        return response

    def post_holding_item(self, data, bib_id, holding_id, q_params={}, raw=False):
        """Creates new item for for a Bib/holding record.

        Args:
            data (xml/str): This method takes a Holding object.
                Note: JSON is not supported for this API.
            bib_id (str): The bib ID (mms_id).
            holding_id (str): The Holding Record ID (holding_id).
                May be 'ALL' to retrieve all holdings for a Bib.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Item object created.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += '/holdings/'
        url += (str(holding_id) + "/items")
        object_type = 'item'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        response = self.create(url, data, args, object_type, raw=raw)

        return response


class SubClientBibsCollections(Client):
    """Handles collections"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/collections'
        self.cnxn_params['api_uri_full'] += '/collections'

    def get(self, pid=None, query={}, q_params={}, raw=False):
        """Returns meta data about collections in libraries.
            If pid argument is used, will only return one collection.

        Args:
            pid (str): The collection ID.
            query (dict): Search query for filtering list. Optional.
                Searching for words from fields: [library, collection name, external system, external ID].
                Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
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

        if query:
            args['q'] = self.__format_query__(query)

        response = self.read(url, args, raw=raw)
        return response

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

        return self.read(url, args, raw=raw)

    def post(self, data, record_format='marc21', q_params={}, raw=False):
        """Creates a new collection.

        Args:
            data (xml/json/str): A Collection object.
            record_format (str): The record format which may be marc21, unimarc,
                kormarc, cnmarc, dc, dcap01, or dcap02.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Collection object created.

        """
        url = self.cnxn_params['api_uri_full']
        object_type = 'collection'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['record_format'] = record_format

        response = self.create(url, data, args, object_type, raw=raw)

        return response

    def post_bib(self, data, pid, q_params={}, raw=False):
        """Adds a bibliographic title into a given collection.

        Args:
            data (xml/json/str): A Bib object with only mms_id.
            pid (str): The collection ID.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Bib objected added to collection.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(pid))
        url += '/bibs'

        object_type = 'bib'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        response = self.create(url, data, args, object_type, raw=raw)

        return response


class SubClientBibsLoans(Client):
    """Accesses loans endpoints"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()

    def get_by_item(self, bib_id, holding_id, item_id,
                    loan_id=None, q_params={}, raw=False):
        """Returns Loan by Item information.

        Args:
            bib_id (str): The bib ID (mms_id).
            holding_id (str): The Holding Record ID (holding_id).
            item_id (str): The holding item ID (item_pid).
            loan_id (str): The loan ID
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of loans or a single loan for a given item.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += ('/holdings/' + str(holding_id))
        url += ('/items/' + str(item_id) + "/loans")
        if loan_id:
            url += ('/' + str(loan_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)

    def get_by_title(self, bib_id, loan_id=None, q_params={}, raw=False):
        """Returns Loan by title information.

        Args:
            bib_id (str): The bib ID (mms_id).
            loan_id (str): The loan ID
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of loans or a single loan for a given title.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id) + '/loans')
        if loan_id:
            url += ('/' + str(loan_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)

    def post(self, data, bib_id, holding_id, item_id, user_id, q_params={}, raw=False):
        """Creates a loan record to a user.
        The loan will be created according to the library's policy.

        Args:
            data (xml/json/str): A Loan object.
            bib_id (str): The bib ID (mms_id).
            holding_id (str): The Holding Record ID (holding_id).
            item_id (str): The holding item ID (item_pid).
            user_id (str): The unique identifier of the loaning user.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Loan object created.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += ('/holdings/' + str(holding_id))
        url += ('/items/' + str(item_id) + "/loans")

        object_type = 'item_loan'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['user_id'] = str(user_id)

        response = self.create(url, data, args, object_type, raw=raw)

        return response


class SubClientBibsRequests(Client):
    """Accesses user request endpoints"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()

    def get_by_item(self, bib_id, holding_id, item_id,
                    request_id=None, q_params={}, raw=False):
        """Returns Loan by Item information.

        Args:
            bib_id (str): The bib ID (mms_id).
            holding_id (str): The Holding Record ID (holding_id).
            item_id (str): The holding item ID (item_pid).
            request_id (str): The loan ID
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of loans or a single loan for a given item.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += ('/holdings/' + str(holding_id))
        url += ('/items/' + str(item_id) + "/requests")
        if request_id:
            url += ('/' + str(request_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)

    def get_by_title(self, bib_id, request_id=None, q_params={}, raw=False):
        """Returns Loan by title information.

        Args:
            bib_id (str): The bib ID (mms_id).
            request_id (str): The loan ID
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of loans or a single loan for a given title.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id) + '/requests')
        if request_id:
            url += ('/' + str(request_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)

    def get_availability(self, bib_id, period, period_type='days',
                         holding_id=None, item_id=None, q_params={}, raw=False):
        """Returns list of periods in which specific title or item
        is unavailable for booking.

        To get a specific item, holding_id and item_id parameters are required.

        Note: user_id does not populate if retrieving by just bid_id.

        Args:
            bib_id (str): The bib ID (mms_id).
            period (str or int): The number of days/weeks/months to retrieve availability for.
            period_type (str): 	The type of period of interest. Optional. Possible values: days, weeks, months.
            holding_id (str): The Holding Record ID (holding_id).
            item_id (str): The holding item ID (item_pid).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of periods title/item is unavailable for booking.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        if holding_id and item_id:
            url += ("/holdings/" + str(holding_id))
            url += ('/items/' + str(item_id))
        elif holding_id or item_id:
            message = "If getting availability for an item, "
            message += "Both holding_id and item_id are required arguments."
            raise utils.ArgError(message)
        url += "/booking-availability"

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['period'] = str(period)
        args['period_type'] = str(period_type)

        return self.read(url, args, raw=raw)

    def get_options(self, bib_id, user_id='GUEST',
                    holding_id=None, item_id=None,
                    q_params={}, raw=False):
        """Returns request options for a specific title or item based on user.

        To get a specific item, holding_id and item_id parameters are required.

        Note: user_id does not populate if retrieving by just bid_id.

        Args:
            bib_id (str): The bib ID (mms_id).
            user_id (str): The id of the user for which the request options will be calculated.
            holding_id (str): The Holding Record ID (holding_id).
            item_id (str): The holding item ID (item_pid).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Request options for a specific title or item based on user.
        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        if holding_id and item_id:
            url += ("/holdings/" + str(holding_id))
            url += ('/items/' + str(item_id))
        elif holding_id or item_id:
            message = "If getting request options for an item, "
            message += "Both holding_id and item_id are required arguments."
            raise utils.ArgError(message)
        url += "/request-options"

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['user_id'] = str(user_id)

        return self.read(url, args, raw=raw)

    def post_for_title(self, data, bib_id, user_id=None, q_params={}, raw=False):
        """Creates a request for a library resouce.
        The request can be for a physical item (request types: hold, booking),
        or a request for digitizing a file (request type: digitization)

        Args:
            data (xml/json/str): A Loan object.
            bib_id (str): The bib ID (mms_id).
            user_id (str): The unique identifier of the loaning user.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Loan object created.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += ('/requests')

        object_type = 'user_request'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        if user_id:
            args['user_id'] = str(user_id)

        response = self.create(url, data, args, object_type, raw=raw)

        return response

    def post_for_item(self, data, bib_id, holding_id,
                      item_id, user_id=None, q_params={}, raw=False):
        """Creates a request for a library resouce.
        The request can be for a physical item (request types: hold, booking),
        or a request for digitizing a file (request type: digitization)

        Args:
            data (xml/json/str): A Loan object.
            bib_id (str): The bib ID (mms_id).
            holding_id (str): The holding id of the record.
            item_id (str): The holding item ID (item_pid).
            user_id (str): The unique identifier of the loaning user.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Loan object created.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += ('/holdings/' + holding_id)
        url += ('/items/' + item_id + "/requests")

        object_type = 'user_request'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        if user_id:
            args['user_id'] = str(user_id)

        response = self.create(url, data, args, object_type, raw=raw)

        return response


class SubClientBibsRepresentations(Client):
    """Handles Digital Representations"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()

    def get(self, bib_id, q_params={}, raw=False):
        """Returns a list of Digital Representations for a given Bib MMS-ID.

        Args:
            bib_id (str): The bib ID (mms_id).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            A list of Digital Representations for a given bib record.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += "/representations"

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)

    def get_details(self, bib_id, rep_id, files=False, q_params={}, raw=False):
        """Returns a specific Digital Representation's details.
        Supported for Remote and Non-Remote Representations.

        Args:
            bib_id (str): The bib ID (mms_id).
            rep_id (str): The Representation ID.
            files (bool): Denote whether to return files?
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            A list of Digital Representations for a given bib record.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += "/representations/"
        url += rep_id
        if files:
            url += "/files"

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)

    def post(self, data, bib_id, generate_label=False, q_params={}, raw=False):
        """Creates a digital representation for a bib record.

        Args:
            data (xml/json/str): A Loan object.
            bib_id (str): The bib ID (mms_id).
            generate_label (bool): Auto-generate label: true/false
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Representation object.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id) + '/representations/')

        object_type = 'representation'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['generate_label'] = generate_label

        response = self.create(url, data, args, object_type, raw=raw)

        return response

    def post_file(self, data, bib_id, rep_id, q_params={}, raw=False):
        """Creates a file for a digital representation.

        Args:
            data (xml/json/str): A Loan object.
            bib_id (str): The bib ID (mms_id).
            rep_id  (str): The representation id.
            generate_label (bool): Auto-generate label: true/false
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Representation object.

        """
        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(bib_id))
        url += ('/representations/' + str(rep_id) + "/files")

        object_type = 'representation'

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        response = self.create(url, data, args, object_type, raw=raw)

        return response


class SubClientBibsLinkedData(Client):
    """Handles Linked Data for a Bib Record"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()

    def get(self, bib_id, q_params={}, raw=False):
        """Returns Linked data for a given Bib MMS-ID.

        Args:
            bib_id (str): The bib ID (mms_id).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            Linked data URIs for a given bib record.

        """
        url = self.cnxn_params['api_uri_full']
        url += "/linked-open-data"
        url += ("/" + str(bib_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)
