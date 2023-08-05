# Google services API in Python
Python sdk that allows extracting data from Google services via [OutScraper API](http://outscraper.com).

## Quick start

```python
from outscraper import ApiClient
api_cliet = ApiClient(api_key='SECRET_API_KEY')
maps_result = api_cliet.google_maps_search('restaurants brooklyn usa')
search_result = api_cliet.google_search('bitcoin')
```