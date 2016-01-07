__author__ = 'yamin'
from .session import get_session
from .base_model import ModelBase
import logging
LOG = logging.getLogger(__name__)

class BaseOperate():
    _session=None
    @property
    def session(self):
        if self._session:
            return self._session
        else:
            return get_session()
    @property
    def query(self):
        current_class=self.__class__
        return self.session.query(current_class)

    def getObjFromDict(self,obj, jsonDict):
        '''
        将一个字典对象转换为Modelbase的对象，且如果该字典key为外键，则外键格式为  外键名.外键对象.对象属性
        :param obj:
        :param jsonDict:
        :return:
        '''
        if jsonDict and isinstance(obj,ModelBase):
            for (key, value) in jsonDict.items():
                if hasattr(obj, key):
                    obj[key] = value
                else:#是一个外键
                    if len(key.split("."))>2:
                        current_key=key.split(".")[0]
                        klass=eval(key.split(".")[1])
                        innerkey=key.split(".")[2]
                        foreign_obj=self.session.query(klass).filter_by(**{innerkey:value}).first()
                        if hasattr(obj,current_key):
                            obj[current_key]=foreign_obj.id
                        else:
                            return False
                    else:
                        return False
            return obj

    def getDictFromObj_nr(self,obj):
        '''
        obj为ModelBase的实例，取obj中所有列的值，relation除外
        :param obj:
        :return:
        '''
        return_dict={}
        if isinstance(obj,ModelBase):
            for key in obj.__dict__ :
                if key.startswith('_'):continue
                return_dict[key]=getattr(obj,key)
        return return_dict

    def getDictFromObj_rp(self,obj,rp_list={}):
        '''
        obj为ModelBase的实例，取obj中所有列的值，relation除外,rp_list里面的对象替换为对象中的某个值
        :param obj:
        :param rp_list: 为relation关系所获取的唯一对象，一般为外键对应的对象
        :return:
        '''
        return_dict=self.getDictFromObj_nr(obj)
        for key in rp_list:
            if hasattr(obj,key):
                sub_obj=getattr(obj,key)
                if isinstance(sub_obj,ModelBase):
                    if hasattr(sub_obj,rp_list[key]):
                        return_dict[key]=getattr(sub_obj,rp_list[key])
        return return_dict

    def getDictFromObj(self,obj):
        '''
        obj为ModelBase的实例，取obj中所有列的值，包括relation所获取的对象或者对象列表
        :param obj:
        :return:
        '''
        return_dict={}
        if isinstance(obj,ModelBase):
            for key in [x for x in dir(obj) if not x.startswith('_') and x not in ["get", "iteritems", "metadata", "next", "save", "update"]]:
                value=getattr(obj,key)
                if isinstance(value,list):#如果是对象列表
                    return_dict[key]=[]
                    for item in value:
                        if isinstance(item,ModelBase):
                            return_dict[key].append(self.getDictFromObj_nr(item))
                        else:
                            return_dict[key].append(item)
                elif isinstance(value,ModelBase):#如果是对象
                    return_dict[key]=self.getDictFromObj_nr(value)
                else:
                    return_dict[key]=getattr(obj,key)
            return return_dict
        else:
            return obj

    def create(self,info):
        '''
        通过info获取ModelBase的对象并保存
        :param info:字典信息，描述了 ModelBase对象的内容
        :return:
        '''
        try:
            obj=self.__class__()
            record=self.getObjFromDict(obj,info)
            self.session.add(record)
            self.session.flush()
            return self.getDictFromObj(record)
        except Exception as e:
            self.session.close()
            LOG.error(str(e))
            raise e

    def update(self,info):
        '''
        通过info获取ModelBase的对象并更新
        :param info: 字典信息，拥有key字典，以及其他信息描述了需要更新的ModelBase对象的内容
        :return:
        '''
        try:
            key_params=info.pop("key")
            self.session.begin()
            record=self.session.query(self.__class__).filter_by(**key_params).first()
            record.update(info)
            self.session.commit()
            return self.getDictFromObj(record)
        except Exception as e:
            self.session.close()
            LOG.error(str(e))
            raise e

    def detail(self,info):
        '''
        通过info获取ModelBase的对象
        :param info: 拥有key信息
        :return:
        '''
        try:
            key_params=info.pop("key")
            record=self.session.query(self.__class__).filter_by(**key_params).first()
            return self.getDictFromObj(record)
        except Exception as e:
            self.session.close()
            LOG.error(str(e))
            raise e

    def list(self,info):
        '''
        通过info中的过滤信息，获取列表
        :param info:包括过滤信息
        :return:
        '''
        try:
            query=self.session.query(self.__class__)
            query=self._list_filter(query,info)
            total=query.count()
            if "page" in info:
                query=self._page(query,info)
            records=query.all()
            return [self.getDictFromObj_nr(item) for item in records],total
        except Exception as e:
            LOG.error(str(e))
            raise e

    def _list_filter(self,query,info):
        try:
            if "join" in info:
                key,value=info["join"].items()[0]
                query=query.join(key).filter(*value)
            if "filter_and" in info:#使用语句来过滤
                sql_word=" and ".join([key for key in info["filter_and"]])
                params=dict([value for key,value in info["filter_and"].items() if value !=""])
                query=query.filter(sql_word).params(**params)
            if "filter_expression" in info:#使用表字段表达式过滤
                query=query.filter(*info["filter_expression"])
            if "order_by" in info:
                query=query.order_by(*info["order_by"])
            return query
        except Exception as e:
            LOG.error(str(e))
            raise e

    def _page(self,query,info):
        if "page" in info:#使用分页
            offset=info["page"]["offset"]
            limit=info["limit"]["limit"]
            query=query.offset(offset).limit(limit)
        return query

class WorkOrderOperate(BaseOperate):
    '''
    订单操作
    '''

class WorkOrderRecordOperate(BaseOperate):
    '''
    订单记录操作
    '''

class WorkOrderTypeOperate(BaseOperate):
    '''
    订单类型操作
    '''