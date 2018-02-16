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
| [acquisitions](#access-acquisitions) | X | | | |
| [configuration](#access-configuration-settings) | X | | | |
| [courses](#access-courses) | X | | | |
| [resource sharing partners](#access-resource-sharing-partners) | X | | | |
| task-lists | | | | |
| [users](#access-users) | X | | | |
| [electronic](#electronic) | X | | | |

## Use

### Import
```python
# Import and call primary Client class
from almapipy import AlmaCnxn
alma = AlmaCnxn('your_api_key', format='json')
```
### Access Bibliographic Data
Alma provides a set of Web services for handling bibliographic records related information, enabling you to quickly and easily manipulate bibliographic records related details. These Web services can be used by external systems to retrieve or update bibliographic records related data.
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
The Analytics API returns an Alma report.
```python
# Find the system path to the report if don't know path
alma.analytics.paths.get('/shared')

# retrieve the report as an XML ET element (native response)
report = alma.analytics.reports.get('path_to_report')

# or convert the xml to json after API call
report = alma.analytics.reports.get('path_to_report', return_json = True)
```

### Access Courses
Alma provides a set of Web services for handling courses and reading lists related information, enabling you to quickly and easily manipulate their details. These Web services can be used by external systems such as Courses Management Systems to retrieve or update courses and reading lists related data.
```python
# Get a complete list of courses. Makes multiple calls if necessary.
course_list = alma.courses.get(all_records = True)

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
Alma provides a set of Web services for handling user information, enabling you to quickly and easily manipulate user details. These Web services can be used by external systems—such as student information systems (SIS)—to retrieve or update user data.
```python
# Get a list of users or filter on search parameters
users = alma.users.get(query = {'first_name': 'Sterling', 'last_name': 'Archer'})

# get more information on that user
user_id = users['user'][0]['primary_id']
alma.users.get(user_id)

# get all loans or requests for a user. Makes multiple calls if necessary.
loans = alma.user.loans.get(user_id, all_records = True)
requests = alma.user.requests.get(user_id, all_records = True)

# get deposits or fees for a user
deposits = alma.users.deposits.get(user_id)
fees = alma.users.fees.get(user_id)
```
### Access Acquisitions
Alma provides a set of Web services for handling acquisitions information, enabling you to quickly and easily manipulate acquisitions details. These Web services can be used by external systems - such as subscription agent systems - to retrieve or update acquisitions data.
```python
# get all funds
alma.acq.funds.get(all_records=True)

# get po_lines by search
amazon_lines = alma.acq.po_lines.get(query={'vendor_account': 'AMAZON'})
single_line_id = amazon_lines['po_line'][0]['number']
# or by a specific line number
alma.acq.po_lines.get(single_line_id)

# search for a vendor
alma.acq.vendors.get(status='active', query={'name':'AMAZON'})
# or get a specific vendor
alma.acq.vendors.get('AMAZON.COM')

# get invoices or polines for a specific vendor
alma.acq.vendors.get_invoices('AMAZON.COM')
alma.acq.vendors.get_po_lines('AMAZON.COM')

# or get specific invoices
alma.acq.invoices.get('invoice_id')

# get all licenses
alma.acq.licenses.get(all_records=True)
```
### Access Configuration Settings
Alma provides a set of Web services for handling Configuration related information, enabling you to quickly and easily receive configuration details. These Web services can be used by external systems in order to get list of possible data.
```python
# Get libraries, locations, departments, and hours
libraries = alma.conf.units.get_libaries()
library_id = libraries['library'][0]['code']
locations = alma.conf.units.get_locations(library_id)
hours = alma.conf.general.get_hours(library_id)
departments = alma.conf.units.get_departments()

# Get system code tables
table = 'UserGroups'
alma.conf.general.get_code_table(table)

# Get scheduled jobs and run history
jobs = alma.conf.jobs.get()
job_id = jobs['job'][0]['id']
run_history = alma.conf.jobs.get_instances(job_id)

# Get sets and set members
sets = alma.conf.sets.get()
set_id = sets['set'][0]['id']
set_members = alma.conf.sets.get_members(set_id)

# get profiles and reminders
depost_profiles = alma.conf.deposit_profiles.get()
import_profiles = alma.conf.import_profiles.get()
reminders = alma.conf.reminders.get()
```
### Access Resource Sharing Partners
Alma provides a set of Web services for handling Resource Sharing Partner information, enabling you to quickly and easily manipulate partner details. These Web services can be used by external systems to retrieve or update partner data.
```python
# get partners
partners = alma.partners.get()
```
### Electronic
Alma provides a set of Web services for handling electronic information, enabling you to quickly and easily manipulate electronic details. These Web services can be used by external systems in order to retrieve or update electronic data.
```python
# get e-collections
collections = alma.electronic.collections.get()
collection_id = collections['electronic_collection'][0]['id']

# get services for a collection
services = alma.electronic.services.get(collection_id)
service_id = services['electronic_service'][0]['id']

# get portfolios for a service
alma.electronic.portfolios.get(collection_id, service_id)

```
## Attribution and Contact


* **Author**: [Steve Pelkey](mailto:spelkey@ucdavis.edu)
