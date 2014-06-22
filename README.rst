Unicoder
========

Handles unicode conversion and normalization and encoding detection.

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


Handling encoding errors and force detecting using ``chardet`` (The Universal Character Encoding Detector)
and decoding using ``beautiful soup`` unicode dammit.

.. code-block:: python

    from unicoder import guess_encoding, force_unicode

    #beer mug sign
    >>> unicode_beer = u"\U0001F37A"
    >>> utf16_beer = encoded(unicode_beer, encoding='utf-16')

    >>> decoded(utf16_beer)
    UnicodeDecodeError("'utf8' codec can't decode byte 0xff in position 0: invalid start byte")

    >>> guess_encoding(utf16_beer)
    'utf-16le'
    assert force_unicode(utf16_beer) == unicode_beer


It happens in web pages to have text not encoded with the declared encoding.
&#127866; &#x1f37a;
An example is an html document containing text cp1252 gremlins which are added by some Windows applications to documents
marked up as ISO 8859-1(Latin 1) or other encodings or through cut-paste operations:

http://johnglotzer.blogspot.co.uk/2013/08/dealing-with-smart-quotes-and-other.html.

These characters are not valid ISO-8859-1 characters, and may cause all sorts of problems in processing
and display applications.

.. code-block:: python


    >>> value = 'foo \x93bar bar \x94 weasel'
    UnicodeDecodeError("'utf8' codec can't decode byte 0x93 in position 4: invalid start byte")

    >>> guess_encoding(value)
    'iso-8859-2'

Text decoded in ``iso-8859-2`` is not correct

.. code-block:: python

    >>> decoded(value, 'iso-8859-2')
    u'foo bar weasel'

Should rather be:

.. code-block:: python

    >>> decoded(value, 'windows-1252')
    u'foo “bar bar ” weasel'

Chardet or beautiful soup will detect the encoding as 'iso-8859-2', however we can figure out that text contains gremlins


.. code-block:: python

    from unicoded.cp1252 import gremlins

    >>> gremlins(decoded(value, 'iso-8859-2'))
    frozenset([u'\x93', u'\x94'])

    >>> guess_encoding(value)
    'windows-1252'

Thus it gets correctly converted to unicode

.. code-block:: python

    >>> force_unicode(value)
    u'foo “bar bar ” weasel'


Normalization
=============

Different ways to represent same letter

.. code-block:: python

    hakan1 = u'HA\u030akan HA\u030akansson'
    u'HÅkan HÅkansson'
    hakan2 = u'H\xc5kan H\xc5kansson'
    u'HÅkan HÅkansson'

    assert not hakan1 == hakan2
    #NFC by default
    assert normalize_unicode(hakan1) == hakan2
