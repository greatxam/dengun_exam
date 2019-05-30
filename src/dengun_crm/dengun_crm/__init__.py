# Created by Maximillian M. Estrada on 30-May-2019

from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ('celery_app',)
