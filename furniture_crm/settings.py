from .common_settings import *  # pylint: disable=W0401


INSTALLED_APPS += [
    'user',
    'core',
    'log',
]


try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass
