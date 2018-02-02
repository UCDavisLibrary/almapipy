# almapipy: Python Wrapper for Alma API

almapipy is python requests wrapper for easily accessing the Ex Libris Alma API. It is designed to be lightweight, and imposes a structure that mimics the [Alma API architecture](https://developers.exlibrisgroup.com/alma/apis).

## Installation
Version 1.0.0 currently under development. Not available through pip yet.

## Use

### Import
```python
# Instantiate primary Client class
from almapipy import AlmaCnxn()
alma = AlmaCnxn('your_api_key')
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
loans = alma.bibs.loans.get_by_item(harry_potter,holding_id,item_id)

# get requests or availability
alma.bibs.requests.get_by_title(harry_potter)
alma.bibs.requests.get_by_item(harry_potter,holding_id,item_id)
alma.bibs.requests.get_availability(harry_potter, period=20)
```
## Attribution

* **Author**: [Steve Pelkey](mailto:spelkey@ucdavis.edu)
