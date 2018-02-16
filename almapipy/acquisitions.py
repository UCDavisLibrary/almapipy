from .client import Client
from . import utils


class SubClientAcquistions(Client):
    """
    Alma provides a set of Web services for handling acquisitions information,
    enabling you to quickly and easily manipulate acquisitions details.
    These Web services can be used by external systems -
    such as subscription agent systems - to retrieve or update acquisitions data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/acq
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/acq"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/acq"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/d5b14609-b590-470e-baba-9944682f8c7e.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of api
        self.funds = SubClientAcquistionsFunds(self.cnxn_params)
        self.po_lines = SubClientAcquistionsPO(self.cnxn_params)
        self.vendors = SubClientAcquistionsVendors(self.cnxn_params)
        self.invoices = SubClientAcquistionsInvoices(self.cnxn_params)
        self.licenses = SubClientAcquistionsLicenses(self.cnxn_params)


class SubClientAcquistionsFunds(Client):
    """Handles the Funds endpoints of Acquisitions API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/funds'
        self.cnxn_params['api_uri_full'] += '/funds'

    def get(self, limit=10, offset=0, library=None, all_records=False,
            q_params={}, raw=False):
        """Retrieve a list of funds.

        Args:
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            library (str): The code of the library that owns the PO line
                for which the relevant funds should be retrieved.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of funds.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        url = self.cnxn_params['api_uri_full']
        args['limit'] = limit
        args['offset'] = int(offset)

        if library:
            args['library'] = str(library)

        response = self.read(url, args, raw=raw)

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='fund')
        return response


class SubClientAcquistionsPO(Client):
    """Handles the PO Lines endpoints of Acquisitions API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/po-lines'
        self.cnxn_params['api_uri_full'] += '/po-lines'

    def get(self, po_line_id=None, query={}, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list or a single PO-Line.

        Args:
            po_line_id (str): 	The PO-Line number ('number' field in record).
            query (dict): Search query for filtering a user list. Optional.
                Searching for words from fields: [title, author, mms_id,
                publisher, publication_year, publication_place, issn_isbn,
                shelving_location, vendor_code, vendor_name, vendor_account,
                fund_code, fund_name, number, po_number, invoice_reference & all].
                Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'vendor_account': 'AMAZON'}
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of po-lines or a specific po-line.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if po_line_id:
            url += ("/" + str(po_line_id))
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
        if po_line_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='po_line')
        return response

    def get_items(self, po_line_id, q_params={}, raw=False):
        """Retrieve a list items related to a specific PO-line

        Args:
            po_line_id (str): 	The PO-Line number ('number' field in record).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of items in PO-Line

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(po_line_id) + "/items")

        response = self.read(url, args, raw=raw)
        return response


class SubClientAcquistionsVendors(Client):
    """Handles the Vendor endpoints of Acquisitions API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/vendors'
        self.cnxn_params['api_uri_full'] += '/vendors'

    def get(self, vendor_id=None, status='ALL', type_='ALL',
            query={}, limit=10, offset=0, all_records=False,
            q_params={}, raw=False):
        """Retrieve a vendor list or a single vendor.

        Args:
            vendor_id (str): A unique identifier for the user (vendorCode).
            status (str): Vendor Status. Valid values: [active, inactive, ALL].
            type_ (str): Vendor Type.Valid values: [material_supplier,
                access_provider, licensor, governmental].
            query (dict): Search query for filtering a user list. Optional.
                Searching for words from fields: [nterface_name, name, code, library & all.].
                Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'name': 'AMAZON'}
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of vendor or a specific vendor's details.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if vendor_id:
            url += ("/" + str(vendor_id))
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
            args['status'] = str(status)
            args['type'] = str(type_)

            # add search query if specified in desired format
            if query:
                args['q'] = self.__format_query__(query)

        response = self.read(url, args, raw=raw)
        if vendor_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='vendor')
        return response

    def get_invoices(self, vendor_id, limit=10, offset=0, all_records=False,
                     q_params={}, raw=False):
        """Retrieve invoices for a specific vendor.

        Args:
            vendor_id (str):  A unique identifier for the user (vendorCode).
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            library (str): The code of the library that owns the PO line
                for which the relevant funds should be retrieved.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of invoices for vendor.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += "/" + (str(vendor_id))
        url += "/invoices"

        if int(limit) > 100:
            limit = 100
        elif int(limit) < 1:
            limit = 1
        else:
            limit = int(limit)
        args['limit'] = limit
        args['offset'] = int(offset)

        response = self.read(url, args, raw=raw)

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='invoice')
        return response

    def get_po_lines(self, vendor_id, limit=10, offset=0, all_records=False,
                     q_params={}, raw=False):
        """Retrieve po-lines for a specific vendor.

        Args:
            vendor_id (str):  A unique identifier for the user (vendorCode).
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            library (str): The code of the library that owns the PO line
                for which the relevant funds should be retrieved.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of po-lines for vendor.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += "/" + (str(vendor_id))
        url += "/po-lines"

        if int(limit) > 100:
            limit = 100
        elif int(limit) < 1:
            limit = 1
        else:
            limit = int(limit)
        args['limit'] = limit
        args['offset'] = int(offset)

        response = self.read(url, args, raw=raw)

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='po_line')
        return response


class SubClientAcquistionsInvoices(Client):
    """Handles the Invoices endpoints of Acquisitions API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/invoices'
        self.cnxn_params['api_uri_full'] += '/invoices'

    def get(self, invoice_id=None, query={}, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list or a single invoice.

        Args:
            invoice_id (str): 	The invoice id.
            query (dict): Search query for filtering a user list. Optional.
                Searching for words from fields: [invoice_number, vendor_code].
                Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'vendor_code': 'AMAZON'}
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of invoices or specific invoice.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if invoice_id:
            url += ("/" + str(invoice_id))
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
        if invoice_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='invoice')
        return response


class SubClientAcquistionsLicenses(Client):
    """Handles the Licenses endpoints of Acquisitions API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/licenses'
        self.cnxn_params['api_uri_full'] += '/licenses'

    def get(self, license_id=None, status='ALL', review_status='ALL',
            query={}, limit=10, offset=0, all_records=False,
            q_params={}, raw=False):
        """Retrieve a list or a single license.

        Args:
            license_id (str): The license id (license_code).
            status (str): Valid values are ACTIVE, DELETED, DRAFT, EXPIRED, RETIRED, ALL
            review_status (str): alid values are ALL, and the listed values in LicenseReviewStatuses code table
            query (dict): Search query for filtering licenses. Optional.
                Searching for words from fields: [name, code, licensor].
                Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'name': 'license_name'}
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of licenses or a specific license.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if license_id:
            url += ("/" + str(license_id))
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
            args['status'] = str(status)
            args['review_status'] = str(review_status)

            # add search query if specified in desired format
            if query:
                args['q'] = self.__format_query__(query)

        response = self.read(url, args, raw=raw)
        if license_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='license')
        return response

    def get_amendments(self, license_id, amendment_id=None, q_params={}, raw=False):
        """Retrieve a specific license's amendments.

        Args:
            license_id (str): The license id (license_code).
            amendment_id (str): The amendment id (amendment_code).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of amendments or specific amendment for a license

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += ("/" + str(license_id) + "/amendments")
        if amendment_id:
            url += ("/" + str(amendment_id))

        response = self.read(url, args, raw=raw)
        return response
