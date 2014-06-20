# coding=utf-8
import bs4
from unicoder import force_unicode, _chardet_convert, encoded, decoded, escape_unicode, unescape_unicode, guess_encoding
from unicoder.cp1252 import replace_gremlins, has_gremlins

hakan = u'Håkan Håkansson'
hakan_utf8 = encoded(hakan)
assert decoded(hakan_utf8) == hakan
print hakan_utf8
print escape_unicode(hakan)
assert unescape_unicode(escape_unicode(hakan)) == hakan

#hakan_latin = decoded(hakan, 'latin1')
#print guess_encoding(hakan_utf8)

value = 'foo \x93bar bar \x94 weasel'

#print decoded(value)
print guess_encoding(value)

print value

print
print 'windows-1252: ', value.decode("windows-1252")
print 'iso-8859-2: ', value.decode('iso-8859-2')

print 'chardet: ', _chardet_convert(value)

soupped = bs4.UnicodeDammit(value)
print soupped.original_encoding.lower()
print 'beautiful soup:', soupped.unicode_markup
print 'beautiful soup escaped: ', escape_unicode(soupped.unicode_markup)

if has_gremlins(soupped.unicode_markup):
    print
    soupped_1252 = bs4.UnicodeDammit(value, override_encodings=['windows-1252'])
    print 'bs windows-1252:', soupped_1252.unicode_markup
    print 'Replace gremlins: ', replace_gremlins(soupped.unicode_markup)

print 'forced:', force_unicode(value)
print 'forced escaped: ', escape_unicode(force_unicode(value))