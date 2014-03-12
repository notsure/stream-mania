
Authentication
==============

For authentication OpenID is used. Currently only Google is supported as OpenID
provider.

In order to request authorization the `auth` resource can be called::

    >>> resp = client.get('/api/auth/google')

This endpoints response will contain a redirect to the Google authentication::

    >>> resp.history
    (<Response [302]>, <Response [302]>, <Response [302]>)
