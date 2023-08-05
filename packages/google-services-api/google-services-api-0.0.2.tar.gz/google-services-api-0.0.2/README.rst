Google services API in Python
=============================

Python sdk that allows extracting data from Google services via
`OutScraper API <http://outscraper.com>`__.

Installation
------------

Python 3+

.. code:: bash

    pip install google-services-api

`Link to the python package
page <https://pypi.org/project/google-services-api/>`__

Quick start
-----------

.. code:: python

    from outscraper import ApiClient
    api_cliet = ApiClient(api_key='SECRET_API_KEY')
    maps_result = api_cliet.google_maps_search('restaurants brooklyn usa')
    search_result = api_cliet.google_search('bitcoin')

