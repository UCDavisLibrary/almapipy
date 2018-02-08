# almapipy: Python Wrapper for Alma API

almapipy is python requests wrapper for easily accessing the Ex Libris Alma API. It is designed to be lightweight, and imposes a structure that mimics the [Alma API architecture](https://developers.exlibrisgroup.com/alma/apis).

## Installation
Version 1.0.0 currently under development. Not available through pip yet.

## Progress and Roadmap
First stage is to develop read functionality around all the Alma APIs. Once completed, Post, Put and Delete will follow.

| API | Get | Post | Put | Delete |
| --- | :---: | :---: | :---: | :---: |
| [bibs](#access-bibliographic-data) | X | | | |
| [analytics](#access-reports) | X | | | |
| acquisitions | | | | |
| configuration | | | | |
| courses | | | | |
| resource sharing partners | | | | |
| task-lists | | | | |
| users | | | | |
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

# get loans
loans = alma.bibs.loans.get_by_title(harry_potter)
# or
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
# Find the system path to the report
alma.analytics.paths.get('/shared')

# retrieve the report as an XML ET element
report = alma.analytics.reports.get('path_to_report')
```
## Attribution and Contact

* **Author**: [Steve Pelkey](mailto:spelkey@ucdavis.edu)
