__author__ = 'yamin'
import oslo_config.cfg as cfg
import sqlalchemy
import logging
import time
import sqlalchemy.orm.session.Session as Session
import sqlalchemy.orm.query.Query as Query
CONF = cfg.CONF
LOG = logging.getLogger(__name__)
_database=[
    cfg.DictOpt('database',
                default={
                    "type":"mysql",
                    "connection_uri":"",#数据库连接字符串
                    "encoding":"utf-8",#数据库编码字符串
                    "pool_size":"5", #连接线程池
                    "max_retry":"10", #最大重试次数
                    "retry_interval":"10", #重试间隔
                },
                help=''),
    ]
_debug=[cfg.BoolOpt('debug',default=True,help=''),]

CONF.register_opts(_database)
CONF.register_opts(_debug)


def _is_db_connection_error(args):
    """Return True if error in connecting to db."""
    # NOTE(adam_g): This is currently MySQL specific and needs to be extended
    #               to support Postgres and others.
    conn_err_codes = ('2002', '2003', '2006')
    for err_code in conn_err_codes:
        if args.find(err_code) != -1:
            return True
    return False

from sqlalchemy.interfaces import PoolListener
class MysqlListener(PoolListener):
    '''
    mysql数据库连接池事件监听
    '''

class SqliteListener(PoolListener):
    '''
    sqlite数据库连接池事件监听
    '''

class PsqlListener(PoolListener):
    '''
    postgresql  数据库连接池事件监听
    '''

def create_engine():
    '''
    根据配置文件创建引擎
    :return:
    '''
    engine_kwargs={
        "echo": CONF._debug,
        'convert_unicode': True,
        "pool_size":CONF._database["pool_size"],
        "encoding":CONF._database["encoding"]
    }
    if CONF._database["type"]=="mysql":
        engine_kwargs["listeners"]=[MysqlListener()]
    elif CONF._database["type"]=="sqlite":
        engine_kwargs["listeners"]=[SqliteListener()]
    elif CONF._database["type"]=="postgresql":
        engine_kwargs["listeners"]=[PsqlListener()]
    engine = sqlalchemy.create_engine(CONF._database["connection_uri"], **engine_kwargs)
    try:
        engine.connect()
    except Exception as e:
        if not _is_db_connection_error(e.args[0]):
            raise
        remaining = CONF.database["max_retry"]
        if remaining == -1:
            remaining = 'infinite'
        while True:
            msg = 'SQL connection failed. %s attempts left.'
            logging.info(msg % remaining)
            if remaining != 'infinite':
                remaining -= 1
            time.sleep(CONF.database["retry_interval"])
            try:
                engine.connect()
                break
            except Exception as e:
                if (remaining != 'infinite' and remaining == 0) or not _is_db_connection_error(e.args[0]):
                    raise
    return engine

_engine=create_engine()

def get_session():
    '''
    自动跟踪对象的改变，并可以使用 flush 立即保存结果。
    :return:
    '''
    session=sqlalchemy.orm.sessionmaker(bind=_engine,class_=Session,autocommit=True,expire_on_commit=True,query_cls=Query)
    return session
