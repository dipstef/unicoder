_cp1252_encodings = ['windows-1252', 'iso-8859-1', 'iso-8859-2']


def is_cp1252(encoding):
    return bool(encoding) and encoding.lower() in _cp1252_encodings


def unicode_to_cp1252(text):
    text_codes = frozenset(text)

    for unicode_code, cp1252_code in cp1252.iteritems():
        if unicode_code in text_codes:
            text = text.replace(unicode_code, cp1252_code)
    return text
    
cp1252 = {
    # from http://www.microsoft.com/typography/unicode/1252.htm
    u"\u20AC": u"\x80", # EURO SIGN
    u"\u201A": u"\x82", # SINGLE LOW-9 QUOTATION MARK
    u"\u0192": u"\x83", # LATIN SMALL LETTER F WITH HOOK
    u"\u201E": u"\x84", # DOUBLE LOW-9 QUOTATION MARK
    u"\u2026": u"\x85", # HORIZONTAL ELLIPSIS
    u"\u2020": u"\x86", # DAGGER
    u"\u2021": u"\x87", # DOUBLE DAGGER
    u"\u02C6": u"\x88", # MODIFIER LETTER CIRCUMFLEX ACCENT
    u"\u2030": u"\x89", # PER MILLE SIGN
    u"\u0160": u"\x8A", # LATIN CAPITAL LETTER S WITH CARON
    u"\u2039": u"\x8B", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u"\u0152": u"\x8C", # LATIN CAPITAL LIGATURE OE
    u"\u017D": u"\x8E", # LATIN CAPITAL LETTER Z WITH CARON
    u"\u2018": u"\x91", # LEFT SINGLE QUOTATION MARK
    u"\u2019": u"\x92", # RIGHT SINGLE QUOTATION MARK
    u"\u201C": u"\x93", # LEFT DOUBLE QUOTATION MARK
    u"\u201D": u"\x94", # RIGHT DOUBLE QUOTATION MARK
    u"\u2022": u"\x95", # BULLET
    u"\u2013": u"\x96", # EN DASH
    u"\u2014": u"\x97", # EM DASH
    u"\u02DC": u"\x98", # SMALL TILDE
    u"\u2122": u"\x99", # TRADE MARK SIGN
    u"\u0161": u"\x9A", # LATIN SMALL LETTER S WITH CARON
    u"\u203A": u"\x9B", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u"\u0153": u"\x9C", # LATIN SMALL LIGATURE OE
    u"\u017E": u"\x9E", # LATIN SMALL LETTER Z WITH CARON
    u"\u0178": u"\x9F", # LATIN CAPITAL LETTER Y WITH DIAERESIS
}