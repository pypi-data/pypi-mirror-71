import warnings

try:
    from . import _snowboydetect
except:
    warnings.warn("snowboy is not properly installed, see snowboy/README.rst", ImportWarning)
