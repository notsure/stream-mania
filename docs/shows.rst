==============
Shows Resource
==============

The shows resource is available to search for new shows a user could subscribe
to.

In order to search for a show use the `/api/shows` endpoint::

    >>> url = '/api/shows/{language}/{name}'
    >>> url = url.format(name='Game of Thrones', language='en')
    >>> resp = client.get(url)
    >>> printjson(resp.content)
    {
        "data": [
            {
                "language": "en", 
                "name": "Game of Thrones", 
                "network": "HBO"
            }
        ], 
        "status": "success"
    }
