"""Contain methods useful when analyzing data."""
import database_util as du
import warnings
warnings.simplefilter('once', DeprecationWarning)


# Deprecated redirects:
def serverAddressSelector(*args, **kwargs):
    """Return output of 'database_util.serverAddressSelector'.

    This keeps backwards compatibilty.
    """
    warnings.warn("Please use 'database_util' directly", DeprecationWarning)
    return du.serverAddressSelector(*args, **kwargs)


def dbColSelector(*args, **kwargs):
    """Return output of 'database_util.dbColSelector'.

    This keeps backwards compatibilty.
    """
    warnings.warn("Please use 'database_util' directly", DeprecationWarning)
    return du.dbColSelector(*args, **kwargs)
