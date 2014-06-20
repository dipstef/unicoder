Unicoder
========

Handles unicode conversion and normalization.
On decoding errors relies to beautiful soup, ``chardet`` to guess the encoding

Conversion
==========
Everything by default is ``utf-8``

.. code-block:: python

    from unicoder import encoded, decoded, escape_unicode, unescape_unicode

    hakan = u'Håkan Håkansson'

    >>> hakan_utf8 = encoded(hakan)
    'Håkan Håkansson'
    assert decoded(hakan_utf8) == hakan

    >>> escape_unicode(hakan)
    'H\xe5kan H\xe5kansson'
    assert unescape_unicode(escape_unicode(hakan)) == hakan


Handling encoding errors and force detecting.
It happens in web pages to have text not encoded with the declared encoding.

An example are cp1252 gremlins that are added by some Windows applications ato documents marked up as ISO 8859-1
(Latin 1) or other encodings. These characters are not valid ISO-8859-1 characters, and may cause all sorts of problems
in processing and display applications.

.. code-block:: python

    from unicoder import guess_encoding, force_unicode

    >>> value = 'foo \x93bar bar \x94 weasel'
    UnicodeDecodeError("'utf8' codec can't decode byte 0x93 in position 4: invalid start byte")

    >>> guess_encoding(value)
    'iso-8859-2'

Text decoded in ``iso-8859-2`` is not correct

.. code-block:: python

    >>> decoded(value, 'iso-8859-2')
    u'foo bar weasel'

Should rather be:

    >>> decoded(value, 'windows-1252')
    u'foo “bar bar ” weasel'