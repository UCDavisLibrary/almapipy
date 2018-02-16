from .client import Client
from . import utils
import xml.etree.ElementTree as ET


class SubClientAnalytics(Client):
    """
    Handles requests to analytics API.
    For more info: https://developers.exlibrisgroup.com/alma/apis/analytics
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/analytics"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/analytics"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/10788916-19f6-4f19-aaf1-c18fa0c31ccd.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']
        self.cnxn_params['xml_ns']['report'] = 'urn:schemas-microsoft-com:xml-analysis:rowset'

        # Hook in subclients of api
        self.paths = SubClientAnalyticsPaths(self.cnxn_params)
        self.reports = SubClientAnalyticsReports(self.cnxn_params)


class SubClientAnalyticsPaths(Client):
    """Handles the path endpoints of analytics API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/paths'
        self.cnxn_params['api_uri_full'] += '/paths'

    def get(self, path=None, q_params={}, raw=False):
        """This API lists the contents of the Alma Analytics report directory.
            If path is not specified, will just return info of root folder.

        Args:
            path (str): folder directory relative to root.
                Does not need to be url encoded.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            ls of directory specificed by path.

        """
        url = self.cnxn_params['api_uri_full']
        if path:
            url += ("/" + str(path))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.read(url, args, raw=raw)


class SubClientAnalyticsReports(Client):
    """Handles the reports endpoints of analytics API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/reports'
        self.cnxn_params['api_uri_full'] += '/reports'

    def get(self, path, _filter=None, limit=25, col_names=True, return_json=False,
            all_records=False, q_params={}, raw=False):
        """This API returns an Alma Analytics report as XML.
        JSON currently unavailable. Use return_json param to convert after the call.

        Args:
            path (str): path of report relative to report root.
                non-URL-encoded. Leave slashes and spaces.
            _filter (str): An XML representation of a filter in OBI format.
                See documentation for more info.
            limit (int): Maximum number of results to return
                Between 25 and 1000 (multiples of 25).
            col_names (bool): Include column heading information.
                To ensure consistent sort order it might be required to turn it off.
            return_json (false): If True, converts xml into json-like structure.
            all_records (bool): Return all rows for a report.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.
                If all_records == True, returns a list.

        Returns:
            XML ET or json-like structure of report,

        """
        url = self.cnxn_params['api_uri_full']

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']
        args['path'] = path
        args['format'] = 'xml'
        args['limit'] = str(int(limit))
        args['col_names'] = col_names
        if _filter:
            args['filter'] = _filter
        row_tag = "{urn:schemas-microsoft-com:xml-analysis:rowset}Row"
        set_tag = "{urn:schemas-microsoft-com:xml-analysis:rowset}rowset"
        columns_tag = "{http://www.w3.org/2001/XMLSchema}element"
        report = self.read(url, args, raw=raw)

        if raw:
            # extract xml from raw response
            # start list with raw responses
            if not all_records:
                return report
            responses = [report]
            report = ET.fromstring(report.text)

        if all_records:
            # check if there are more records to get
            if report[0].find('IsFinished').text == 'false':
                get_more = True

                # just need token and apikey for future calls
                margs = {'apikey': self.cnxn_params['api_key']}
                margs['token'] = report[0].find('ResumptionToken').text
                margs['format'] = 'xml'

                # find report content in XML report
                xml_rows = list(report.iter(set_tag))[0]
            else:
                get_more = False

            # make additional api calls and append rows to original xml
            while get_more:

                report_more = self.read(url, margs, raw=raw)

                if raw:
                    responses += [report_more]
                    report_more = ET.fromstring(report_more.text)

                else:
                    for new_row in report_more.iter(row_tag):
                        xml_rows.append(new_row)

                # break loop if no more records
                if report_more[0].find('IsFinished').text != 'false':
                    get_more = False

        if raw:
            return responses

        if return_json:
            # extract column names
            columns_tag = "{http://www.w3.org/2001/XMLSchema}element"
            columns = list(report.iter(columns_tag))
            headers = {}
            for col in columns:
                key = col.attrib['name']
                try:
                    value = col.attrib['{urn:saw-sql}columnHeading']
                except:
                    value = col.attrib['name']
                value = value.lower().replace(" ", "_")
                headers[key] = value

            # covert to list of dicts
            dicts = []
            rows = report.iter(row_tag)
            for row in rows:
                values = [col.text for col in row]
                keys = [headers[col.tag.split('}')[-1]] for col in row]
                dicts.append({key: value for key, value in zip(keys, values)})
            return dicts

        return report
