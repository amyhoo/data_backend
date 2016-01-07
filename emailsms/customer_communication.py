# -*- coding:utf-8 -*-
__author__ = 'yamin'
from emailsms.email_hand.email_handle import EmailHandle
from emailsms.yuntong.api import sms
from db.session import get_session
from db.models import *
import datetime
from constant.sql import SQL
from oslo_config import cfg
CONF=cfg.CONF
import traceback
from oslo_log import log as logging
LOG = logging.getLogger(__name__)

class NoticeCenter():
    '''
    信息中心,单session
    '''
    _session=None
    @property
    def session(self):
        if not self._session:
            self._session=get_session()
        return self._session

    def _get_today(self):
        return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    def _get_account_info(self,account_id):
        '''
        获取帐号信息
        :param account_id:
        :return:
        '''
        account_info={}
        pass
        return account_info

    def paySuccess(self,order_no,remark=""):
        '''
        根据订单号进行判断以下几种情形，并发送邮件与短信
        1.赠送用户金额，通知客户
        2.用户自己充值完成，通知客户
        3.代理给下线充值完成，通知代理与下线
        4.客服给用户充值完成，通知客户
        order_no:用户号
        info:附加信息
        :return:
        '''
        try:
            info={}
            pass
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.pay_success(info)
            smsSender.pay_success(info)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            raise e

    def lowcashReminder_3(self):

        for account in self.session.query(Account).filter(Account.status=='normal').all():
            self._lowcashReminder_3(account.account_id)

    def _lowcashReminder_3(self,account_id):
        '''
        当前余额比较低的时候提前三天给客户提醒
        :param account_id:客户帐号
        :return:
        '''
        try:
            account=self._get_account_info(account_id)
            consume_3_day=0
            info={}
            pass

            emailSender=EmailHandle()
            smsSender=sms()

            if consume_3_day>account["available_balance"]:
                emailSender.lowcash_reminder(info)
                smsSender.lowcash_reminder(info)

        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())

    def freezen(self,account_id):
        '''
        冻结
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.freeze(info)
            smsSender.freeze(info)
        except Exception as e:
            pass

    def unfreezen(self,account_id):
        '''
        解冻
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),#
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.unfreeze(info)
            smsSender.unfreeze(info)
        except Exception as e:
            pass

    def credit_adjust(self,account_id):
        '''
        调整信用额度
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),#
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.credit_adjust(info)
            smsSender.credit_adjust(info)
        except Exception as e:
            pass

    def update_credit(self,account_id):
        '''
            调整用户类型额度
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),#
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.update_credit(info)
            smsSender.update_credit(info)
        except Exception as e:
            pass

    def del_resource_3(self,account_id,):
        '''
        删除资源提前3天提醒
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),#
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.del3_resource(info)
            smsSender.del3_resource(info)
        except Exception as e:
            pass

    def del_resource(self,account_id):
        '''
        删除资源
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),#
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.del_resource(info)
            smsSender.del_resource(info)
        except Exception as e:
            pass

if __name__=="__main__":
    this_info=NoticeCenter()
    this_info.paySuccess("15124603483901")
    #this_info.freezen("fd6f0af1-9cbc-11e5-be79-fa163ee4b056")
    print ("中文")
    #print ("中文")
    #lowcashReminder_3("fd6f0716-9cbc-11e5-be79-fa163ee4b056")