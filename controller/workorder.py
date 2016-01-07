# -*- coding:utf-8 -*-
'''
Created on 2015-12-18

@author: yamin
账户数据库操作类
'''
from urlmap import wsgi
import json
from oslo_config import cfg
CONF = cfg.CONF
from db.operater import *
from db.models import *
import traceback
from sqlalchemy import desc
import random
import datetime
not_include=["records","type",]

class Controller():

    def _check_params(self,json_dict,params={}):
        if params <= set(json_dict.keys()):
            return True
        else:
            return False

    def create_workorder_type(self,req, *args,**kwargs):
        '''
        创建工单类型
        :param req:
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            info=req.json_body
            self._check_params(info,{})
            db_params={
                "name":info["name"],
                "code":info["code"],
                "remark":info["remark"],

            }
            record=WorkOrderTypeOperate().create(db_params)
            return json.dumps({"workordertype", record})
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("创建工单类型失败！")

    def create_workorder(self,req, *args,**kwargs):
        '''
        创建工单
        '''
        try:
            info=req.json_body
            self._check_params(info,{})
            import datetime
            workorder_no=generation()
            db_params={

            }
            record=WorkOrderOperate().create(db_params)
            return json.dumps("workorder", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("创建工单失败！")

    def create_workorder_record(self,req,*args,**kwargs):
        '''
        创建工单评论
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            info=req.json_body
            self._check_params(info,{})
            db_params={
            }
            if "status" in info:
                db_params["status"]=info["status"] #能够设置处理状态的为管理员
            record1=WorkOrderRecordOperate().create(db_params)
            return_data={"workorderrecord":record1}
            if "status" in info:#更新订单状态
                db_params={
                }
                record2=WorkOrderOperate().update(db_params)
                return_data.update({"workorder":record2})
            return_data.update({"success":"success"})
            return json.dumps(return_data)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("创建工单评论失败！")

    def update_workorder(self,req,*args,**kwargs):
        '''
        处理工单
        :param req:
        :param args:
        :return:
        '''
        try:
            info=req.json_body
            self._check_params(info,{})
            db_params={
                        "key":{
                            "workorder_no":info["workorderno"]
                        },
                        "status":info["status"]
                    }
            record=WorkOrderOperate().update(db_params)
            return json.dumps("workorder", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("更新工单失败！")

    def workorder_detail(self,req,*args,**kwargs):
        '''
        工单详情
        :param req:
        :param args:
        :return:
        '''
        try:
            workorderno=kwargs.get('workorderno')
            db_params={
                "key":{"workorder_no":workorderno,}
            }
            record=WorkOrderOperate().detail(db_params)
            return json.dumps("detail", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("获取工单失败！")

    def workorder_list(self,req,*args,**kwargs):
        '''
        工单列表
        :param req:
        :param args:
        :return:
        '''
        try:
            user=req.params.get('user')
            info={
                "user":user,
                "join":{
                    "condition1"
                },
                "filter_and":{
                  "condition2"

                },
                "filter_expression":[
                    WorkOrder.status==""
                ],

                "page":{
                    "page_no":"",
                    "page_size":""
                },
                "order_by":[desc(WorkOrder.apply_at)]
            }

            pass
            records,total=WorkOrderOperate().list(info)
            return json.dumps({"workorders":records,"total":total,"success":"success"})
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("获取工单列表失败！")

    def workorder_type_list(self,req,*args,**kwargs):
        '''
        工单评论列表
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            records,total=WorkOrderTypeOperate().list({})
            return json.dumps("types",records)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("获取工单类型失败！")

    def workorder_record_list(self,req,*args,**kwargs):
        '''
        工单评论列表
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            workorderno=kwargs.get('workorderno')
            info={
            }
            if not workorderno:
                info.pop("join")
            records,total=WorkOrderRecordOperate().list(info)
            return json.dumps("records", records)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return json.dumps("获取工单记录失败！")
def generation():
    order_id=datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y-%m-%d %H:%M:%S')
    return order_id
