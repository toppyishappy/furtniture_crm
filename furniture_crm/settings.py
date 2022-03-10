from .common_settings import *  # pylint: disable=W0401


INSTALLED_APPS += [
    'compressor',
    'user',
    'core',
    'log',
]
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

try:
    from configs import *  # pylint: disable=W0401
except ImportError:
    pass
