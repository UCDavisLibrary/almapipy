# almapipy: Python Wrapper for Alma API

almapipy is python requests wrapper for easily accessing the Ex Libris Alma API. It is designed to be lightweight, and imposes a structure that mimics the [Alma API architecture](https://developers.exlibrisgroup.com/alma/apis).

## Installation
Version 1.0.0 currently under development. Not available through pip yet.

## Use
```python
# Instantiate primary Client class
from almapipy import AlmaCnxn()
alma = AlmaCnxn('your_api_key')

# get holding items for a bib record
holdings = alma.bibs.catalog.get_holdings('bib_id')
```
## Attribution

* **Author**: [Steve Pelkey](mailto:spelkey@ucdavis.edu)
