from . import handlers
from . import logger
from .log_object import LogObject, ErrorLogObject, SqlLogObject


__version__ = '1.15'
__author__ = 'Ciprian Tarta'

log = logger.get_logger()

