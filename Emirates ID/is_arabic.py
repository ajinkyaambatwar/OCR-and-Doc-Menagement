import unicodedata as ud
arabic_character={}
def is_arabic(uchr):
    try: return arabic_character[uchr]
    except KeyError:
         return arabic_character.setdefault(uchr, 'ARABIC' in ud.name(uchr))

def only_arabic_chars(unistr):
    return all(is_arabic(uchr)
           for uchr in unistr
           if uchr.isalpha()) # isalpha suggested by John Machin

print(only_arabic_chars('8 li\n'))