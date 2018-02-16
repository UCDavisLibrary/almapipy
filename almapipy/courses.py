from .client import Client
from . import utils


class SubClientCourses(Client):
    """
    The Courses API allows access to courses and reading lists related information.
    These Web services can be used by external systems such as Courses Management
    Systems to retrieve or update courses and reading lists related data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/courses
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/courses"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/courses"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/25ede018-da5d-4780-8fda-a8e5d103faba.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']
        #self.cnxn_params['xml_ns']['report'] = 'urn:schemas-microsoft-com:xml-analysis:rowset'

        # Hook in subclients of api
        self.reading_lists = SubClientCoursesReadingLists(self.cnxn_params)
        self.citations = SubClientCoursesCitations(self.cnxn_params)
        self.owners = SubClientCoursesOwners(self.cnxn_params)
        self.tags = SubClientCoursesTags(self.cnxn_params)

    def get(self, course_id=None, query={}, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a courses list or a single course.

        Args:
            course_id (str): The identifier of a single course.
                Gets more detailed information.
            query (dict): Search query for filtering a course list. Optional.
                Searching for words from fields: [code, section, name, notes,
                instructors, searchable_ids, year, academic_department,
                all]. Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'code': 'ECN'} returns a list of econ classes
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of courses or a specific course resource.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        if course_id:
            url += ("/" + str(course_id))
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
        if course_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='course')
        return response


class SubClientCoursesReadingLists(Client):
    """Handles the reading list endpoints of Courses API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, course_id, reading_list_id=None, view='brief', q_params={}, raw=False):
        """Retrieves all Reading Lists, or a specific list, for a Course.

        Args:
            course_id (str): The identifier of the Course.
            reading_list_id (str): The identifier of the Reading List.
            view (str): 'brief' or 'full' view of reading list.
                Only applies when retrieving a single record.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of reading lists or single list
                for a given course ID.
        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += str(course_id)
        url += '/reading-lists'
        if reading_list_id:
            url += ('/' + str(reading_list_id))
            if view not in ['brief', 'full']:
                message = "Valid view arguments are 'brief' or 'full'"
                raise utils.ArgError(message)
            args['view'] = view

        return self.read(url, args, raw=raw)


class SubClientCoursesCitations(Client):
    """Handles the citations endpoints of Courses API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, course_id, reading_list_id, citation_id=None, q_params={}, raw=False):
        """Retrieves all citations, or a specific citation, for a reading list.

        Args:
            course_id (str): The identifier of the Course.
            reading_list_id (str): The identifier of the Reading List.
            citation_id (str): The identifier of the citation.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of citations or single citation
                for a given reading list ID.
        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += str(course_id)
        url += '/reading-lists'
        url += ('/' + str(reading_list_id))
        url += '/citations'

        if citation_id:
            url += ('/' + str(citation_id))

        return self.read(url, args, raw=raw)


class SubClientCoursesOwners(Client):
    """Handles the owners endpoints of Courses API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, course_id, reading_list_id, owner_id=None, q_params={}, raw=False):
        """Retrieves all owners, or a specific owner, for a reading list.

        Args:
            course_id (str): The identifier of the Course.
            reading_list_id (str): The identifier of the Reading List.
            owner_id (str): The primary identifier of the user (primary_id).
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of owner or single owner
                for a given reading list ID.
        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += str(course_id)
        url += '/reading-lists'
        url += ('/' + str(reading_list_id))
        url += '/owners'

        if owner_id:
            url += ('/' + str(owner_id))

        return self.read(url, args, raw=raw)


class SubClientCoursesTags(Client):
    """Handles the citation tags endpoints of Courses API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def get(self, course_id, reading_list_id, citation_id, q_params={}, raw=False):
        """Retrieves a citation's tag list.

        Args:
            course_id (str): The identifier of the Course.
            reading_list_id (str): The identifier of the Reading List.
            citation_id (str): The identifier of the citation.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of a citation's tags in for a given reading list ID.
        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += str(course_id)
        url += '/reading-lists'
        url += ('/' + str(reading_list_id))
        url += '/citations'
        url += ('/' + str(citation_id) + "/tags")

        return self.read(url, args, raw=raw)
