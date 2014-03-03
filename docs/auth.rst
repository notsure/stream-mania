
Authentication
==============

For authentication OpenID is used. Currently only Google is supported as OpenID
provider.

In order to request authorization the `auth` resource can be called::

    >>> resp = client.get('/api/auth/google')

This endpoints response will contain a redirect to the Google authentication::

    >>> resp.history
    (<Response [302]>, <Response [302]>, <Response [302]>)


Whenever a `GET` request is made to any resource that requires authorization a
HTTP-Redirect response is returned::

    >>> resp = client.get('/api/me/profile')
    >>> resp.history

Requests without authorization using other HTTP methods than `GET` will receive
a `403` error code instead of a redirection::

    >>> resp = client.put('/api/me/profile')
    >>> resp.status_code
    403
