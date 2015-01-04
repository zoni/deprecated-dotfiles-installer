# (c) 2013, Nick Groenen <zoni@zoni.nl>

def split(str, sep=None, maxsplit=-1):
    """Return a list of the words in the string, using sep as the delimiter string."""
    return str.split(sep, maxsplit)

class FilterModule(object):

    def filters(self):
        return dict(split=split)