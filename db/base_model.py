__author__ = 'yamin'
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class ModelBase(BASE):
    '''
    基类
    '''