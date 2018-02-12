# almapipy: Python Wrapper for Alma API

almapipy is python requests wrapper for easily accessing the Ex Libris Alma API. It is designed to be lightweight, and imposes a structure that mimics the [Alma API architecture](https://developers.exlibrisgroup.com/alma/apis).

## Installation
Version 1.0.0 currently under development. Not available through pip yet.

## Progress and Roadmap
First stage is to develop read functionality around all the Alma APIs. Once completed, Post, Put and Delete will follow.

| API | Get | Post | Put | Delete |
| --- | :---: | :---: | :---: | :---: |
| [bibs](#access-bibliographic-data) | X | | | |
| [analytics](#access-reports) | X | NA | NA | NA |
| acquisitions | | | | |
| configuration | | | | |
| [courses](#access-courses) | X | | | |
| resource sharing partners | | | | |
| task-lists | | | | |
| [users](#access-users) | X | | | |
| electronic | | | | |

## Use

### Import
```python
# Import and call primary Client class
from almapipy import AlmaCnxn
alma = AlmaCnxn('your_api_key', format='json')
```
### Access Bibliographic Data
```python
# Use Alma mms_id for retrieving bib records
harry_potter = "9980963346303126"
bib_record = alma.bibs.catalog.get(harry_potter)

# get holding items for a bib record
holdings = alma.bibs.catalog.get_holdings(harry_potter)

# get loans by title
loans = alma.bibs.loans.get_by_title(harry_potter)
# or by a specific holding item
loans = alma.bibs.loans.get_by_item(harry_potter, holding_id, item_id)

# get requests or availability of bib
alma.bibs.requests.get_by_title(harry_potter)
alma.bibs.requests.get_by_item(harry_potter, holding_id, item_id)
alma.bibs.requests.get_availability(harry_potter, period=20)

# get digital representations
alma.bibs.representations.get(harry_potter)

# get linked data
alma.bibs.linked_data.get(harry_potter)
```

### Access Reports
```python
# Find the system path to the report if don't know path
alma.analytics.paths.get('/shared')

# retrieve the report as an XML ET element
report = alma.analytics.reports.get('path_to_report')

# or convert the xml to json after API call
report = alma.analytics.reports.get('path_to_report', return_json = True)
```

### Access Courses
```python
# Get a complete list of courses in 1000 record increments
course_list = alma.courses.get(limit = 1000, all_records = True)

# or filter on search parameters
econ_courses = alma.courses.get(query = {'code': 'ECN'})

# get reading lists for a course
course_id = econ_courses['course'][0]['id']
reading_lists = alma.courses.reading_lists.get(course_id)

# get more detailed information about a specific reading list
reading_list_id = reading_lists['reading_list'][0]['id']
alma.courses.reading_lists(course_id, reading_list_id, view = 'full')

# get citations for a reading list
alma.courses.citations(course_id, reading_list_id)
```

### Access Users
```python
# Get a list of users or filter on search parameters
users = alma.users.get(query = {'first_name': 'Sterling', 'last_name': 'Archer'})

# get more information on that user
user_id = users['user'][0]['primary_id']
alma.users.get(user_id)

# get all loans or requests for a user in 100 record increments
loans = alma.user.loans.get(user_id, limit = 100, all_records = True)
requests = alma.user.requests.get(user_id, limit = 100, all_records = True)

# get deposits or fees for a user
deposits = alma.users.deposits.get(user_id)
fees = alma.users.fees.get(user_id)
```
## Attribution and Contact

* **Author**: [Steve Pelkey](mailto:spelkey@ucdavis.edu)
