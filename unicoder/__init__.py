import unicodedata

import bs4
import chardet

from . import cp1252


def encoded(text, encoding='utf-8', ignore_errors=False):
    return text and (text.encode(encoding) if not ignore_errors else text.encode(encoding, 'ignore'))


def decoded(text, encoding='utf-8', ignore_errors=False):
    return text and (text.decode(encoding) if not ignore_errors else text.decode(encoding, 'ignore'))


def normalize_unicode(unicode_text, form='NFC'):
    #Solves the Issue of  characters that can be represented in multiple ways in unicode: u'A\u030a' and u'\xc5'
    return unicodedata.normalize(form, unicode_text)


def escape_unicode(text):
    return unicode(encoded(text, encoding='unicode-escape'))


def unescape_unicode(text):
    return decoded(text, encoding='unicode-escape')


def byte_string(text, encoding='utf-8'):
    return encoded(text, encoding) if isinstance(text, unicode) else _to_str(text)


def _to_str(value):
    return value if isinstance(value, str) else str(value)


def to_unicode(text, encoding='utf-8'):
    return decoded(_to_str(text), encoding) if not isinstance(text, unicode) else text


def to_normalized_unicode(text, form='NFC'):
    return normalize_unicode(to_unicode(text), form)


def guess_encoding(text):
    assert isinstance(text, str)

    encoding = _chardet_encoding(text)

    if cp1252.is_smart_quote_encoding(encoding) and cp1252.has_gremlins(decoded(text, encoding)):
        encoding = 'windows-1252'

    return encoding


def force_unicode(text, encoding='utf-8'):
    try:
        return to_unicode(text, encoding)
    except UnicodeDecodeError:
        return _unicode_dammit(text, guess_encoding(text))


def _unicode_dammit(text, encoding):
    soup = bs4.UnicodeDammit(text, override_encodings=[encoding])
    return soup.unicode_markup


def _chardet_convert(text):
    encoding = _chardet_encoding(text)
    if not encoding:
        raise CanNotConvertToUnicode(text)

    text_decoded = decoded(text, encoding, ignore_errors=True)
    if cp1252.is_smart_quote_encoding(encoding) and cp1252.has_gremlins(text_decoded):
        text_decoded = cp1252.replace_gremlins(text_decoded)

    return text_decoded


def _chardet_encoding(text):
    char_detection = chardet.detect(text)
    encoding = char_detection['encoding']
    return encoding and encoding.lower()


class EncodingError(Exception):
    def __init__(self, text, *args, **kwargs):
        super(EncodingError, self).__init__(*args, **kwargs)
        self.text = text


class CanNotConvertToUnicode(EncodingError):
    def __init__(self, text):
        super(CanNotConvertToUnicode, self).__init__(text, 'Can Not Convert To Unicode: ', text)