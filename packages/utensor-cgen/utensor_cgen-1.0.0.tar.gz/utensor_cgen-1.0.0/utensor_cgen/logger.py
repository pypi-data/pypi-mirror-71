#-*- coding: utf8 -*-
import logging
import os
import sys

__all__ = ['logger']


logger = logging.getLogger(name='utensor-cli')
logger.setLevel(os.environ.get('UTENSOR_LOG_LEVEL', logging.INFO))
_fmt = logging.Formatter(fmt='[%(levelname)s %(filename)s %(funcName)s @ %(lineno)s] %(message)s')
_handler = logging.StreamHandler(sys.stdout)
_handler.formatter = _fmt
logger.addHandler(_handler)
