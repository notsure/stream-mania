===========
Me Resource
===========

The ``/api/me`` resource provides information about the currently logged in
user. If the user isn't logged in it will return with FORBIDDEN::

    >>> resp = client.get('/api/me')
    >>> resp.status_code
    405

If the user is logged in he will receive his username instead::

    >>> client.login()
    >>> resp = client.get('/api/me')
    >>> printjson(resp.content)
    {
        "data": {
            "username": "hoschi"
        }, 
        "status": "success"
    }
