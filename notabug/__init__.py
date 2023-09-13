from os import unlink
from .notabug import compile_from_file
from io import BytesIO
from fontTools.ttLib import TTFont, getTableClass
from fontTools.feaLib.ast import FeatureFile
import tempfile


def addOpenTypeFeatures(font, featurefile, tables=None, debug=False):
    if isinstance(featurefile, FeatureFile):
        return addOpenTypeFeaturesFromString(fnt, featurefile.asFea(), tables=tables)

    newfontbin = BytesIO(compile_from_file(featurefile, font.getGlyphOrder()))
    merge_fonts(font, newfontbin, tables)


def addOpenTypeFeaturesFromString(
    font, features, filename=None, tables=None, debug=False
):
    # Very sad. But saves messing around with resolvers and resolving
    # include files and so on.
    fp = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    fp.write(features)
    fp.close()
    newfontbin = BytesIO(compile_from_file(fp.name, font.getGlyphOrder()))
    unlink(fp.name)
    merge_fonts(font, newfontbin, tables)


def merge_fonts(font, newfontbin, tables):
    newfont = TTFont(newfontbin)

    for tag in newfont.reader.keys():
        if tables and tag not in tables:
            continue
        data = newfont.reader[tag]
        tableClass = getTableClass(tag)
        table = tableClass(tag)
        font.tables[tag] = table
        table.decompile(data, font)
