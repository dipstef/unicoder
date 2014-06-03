import unicodedata

import bs4
import chardet

from .cp1252 import is_cp1252, unicode_to_cp1252


def encoded(text, encoding='utf-8', ignore_errors=False):
    return text and text.encode(encoding) if not ignore_errors else text.encode(encoding, 'ignore')


def decoded(text, encoding='utf-8', ignore_errors=False):
    return text and text.decode(encoding) if not ignore_errors else text.decode(encoding, 'ignore')


def normalize_unicode(unicode_text, form='NFC'):
    #Solves the Issue of  characters that can be represented in multiple ways in unicode: u'A\u030a' and u'\xc5'
    return unicodedata.normalize(form, unicode_text)


def escape_unicode(text):
    return unicode(encoded(text, encoding='unicode-escape'))


def un_escape_unicode(text):
    return decoded(text, encoding='unicode-escape')


def byte_string(text, encoding='utf-8'):
    return encoded(text, encoding) if isinstance(text, unicode) else _to_str(text)


def _to_str(value):
    return value if isinstance(value, str) else str(value)


def to_unicode(text, encoding='utf-8'):
    return decoded(_to_str(text), encoding) if not isinstance(text, unicode) else text


def to_normalized_unicode(text, form='NFC'):
    return normalize_unicode(to_unicode(text), form)


def force_unicode(text, encoding='utf-8'):
    try:
        return to_unicode(text, encoding)
    except UnicodeDecodeError:
        return _force_detect_unicode(text)


def _force_detect_unicode(text):
    #Uses the "unicode damn it" which forces unicode no matter less
    soup = bs4.UnicodeDammit(text, smart_quotes_to=None)

    if is_cp1252(soup.original_encoding):
        return unicode_to_cp1252(soup.unicode_markup)
    else:
        soup_unicode = soup.unicode_markup
        if soup_unicode:
            return soup_unicode
        else:
            #apparently this is silently performed by beautiful soup once chardet is installed
            return _chardet_detect(text)


def _chardet_detect(text):
    char_detection = chardet.detect(text)
    encoding = char_detection['encoding']
    if not encoding:
        raise CanNotConvertToUnicode(text)
    elif is_cp1252(encoding):
        return unicode_to_cp1252(encoding)
    else:
        return decoded(text, encoding, ignore_errors=True)


class EncodingError(Exception):
    def __init__(self, text, *args, **kwargs):
        super(EncodingError, self).__init__(*args, **kwargs)
        self.text = text


class CanNotConvertToUnicode(EncodingError):
    def __init__(self, text):
        super(CanNotConvertToUnicode, self).__init__(text, 'Can Not Convert To Unicode: ', text)