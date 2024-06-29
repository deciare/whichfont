import os
import sys
import unicodedata

if len(sys.argv) != 2:
    print("Usage: %s <character>" % sys.argv[0])
    sys.exit()

collections = []
fonts = []

def append_fonts(files):
    for file in files:
        if file.endswith(".otf") or file.endswith(".ttf"):
           fonts.append(os.path.join(root,file))
        elif file.endswith(".otc") or file.endswith(".ttc"):
           collections.append(os.path.join(root,file))

from pathlib import Path

for root,dirs,files in os.walk("/usr/share/fonts/"):
	append_fonts(files)

for root,dirs,files in os.walk("/System/Library/Fonts/"):
	append_fonts(files)

for root,dirs,files in os.walk("/Library/Fonts/"):
	append_fonts(files)

for root,dirs,files in os.walk(str(Path.home()) + "/Library/Fonts/"):
	append_fonts(files)

from fontTools.ttLib import TTCollection
from fontTools.ttLib import TTFont

def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False

def test(char):
    for fontpath in fonts:
        font = TTFont(fontpath)   # specify the path to the font in question
        if char_in_font(char, font):
            print(char + " "+ unicodedata.name(char) + " in " + fontpath) 
    for collectionpath in collections:
        collection = TTCollection(collectionpath)
        for font in collection.fonts:
            if char_in_font(char, font):
                print(char + " "+ unicodedata.name(char) + " in " + collectionpath) 

test(u"%s" % sys.argv[1])
