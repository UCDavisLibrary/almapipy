# almapipy: Python Wrapper for Alma API

almapipy is python package for easily accessing the Ex Libris Alma API. It is designed to be lightweight, and provides a pythonic structure that mimics the [Alma API documentation](https://developers.exlibrisgroup.com/alma/apis). It is currently under development.
## Use
```python
# Instantiate primary Client class
from almapipy import AlmaCnxn()
alma = AlmaCnxn('your_api_key')

# get holding items for a bib record
holdings = alma.bibs.catalog.get_holdings('bib_id')
```
