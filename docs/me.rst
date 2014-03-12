===========
Me Resource
===========

The ``/api/me`` resource provides information about the currently logged in
user. If the user isn't logged in it will return with FORBIDDEN::

    >>> resp = client.get('/api/me')
    >>> resp.status_code
    403

A potential user doesn't have to create a new account, instead he authenticates
himself using an OpenID provider (currently only Google is supported)::

    >>> client.authenticate()  # see `auth.rst` for real authentication

Once authenticated the user just has to set a username to activate the
account::

    >>> payload = {'username': 'hoschi'}
    >>> resp = client.post('/api/me', data=payload)
    >>> resp.status_code
    200

Afterwards the `/me` resource will return the users username::

    >>> resp = client.get('/api/me')
    >>> printjson(resp.content)
    {
        "data": {
            "username": "hoschi"
        }, 
        "status": "success"
    }

Changing the name afterwards isn't possible::

    >>> payload = {'username': 'superhoschi'}
    >>> resp = client.post('/api/me', data=payload)
    >>> resp.status_code
    400
