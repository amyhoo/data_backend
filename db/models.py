from .base_model import ModelBase
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, DateTime, Boolean, Text, DECIMAL,Column, Integer, String,event

def utcnow():
    import datetime
    return datetime.datetime.utcnow()

class Account(ModelBase):
    __tablename__ = 'account'
    __table_args__ = ()
    pass

'''
地址
'''
class Address(ModelBase):
    __tablename__ = 'address'
    __table_args__ = ()
    pass

'''
账单
'''
class Bill(ModelBase):
    __tablename__ = 'bill'
    __table_args__ = ()
    pass

'''
账单项
'''
class BillItem(ModelBase):
    __tablename__ = 'bill_item'
    __table_args__ = ()
    pass

'''
计费项
'''
class BillingItem(ModelBase):
    __tablename__ = 'billing_item'
    __table_args__ = ()
    pass

'''
折扣
'''
class Discount(ModelBase):
    __tablename__ = 'discount'
    __table_args__ = ()
    pass


'''
消费记录
'''
class Consumption(ModelBase):
    __tablename__ = 'consumption'
    __table_args__ = ()
    pass

'''
发票
'''
class Invoice(ModelBase):
    __tablename__ = 'invoice'
    __table_args__ = ()
    pass

class Order(ModelBase):
    __tablename__ = 'order'
    __table_args__ = ()
    order_no=Column(String(20), primary_key=True)
    account_id=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    payment_type=Column(String(32))
    amount=Column(DECIMAL(8,2))
    status=Column(String(32))
    remark=Column(String(256))

def pay_success_reminder2(order_no):
    '''
    在已经存储到数据库后进行提醒
    :param order_no:
    :return:
    '''
    import emailsms
    def func(session):
        try:
            from emailsms.customer_communication import NoticeCenter
            NoticeCenter().paySuccess(order_no)#target.dict["order_no"]
        except Exception as e:
            pass
        return True
    return func

@event.listens_for(Order, 'after_insert',raw=True)
@event.listens_for(Order, 'after_update',raw=True)
def pay_success_reminder1(mapper, connection, target):#
    '''
     已经充值成功，给用户发送提醒
    :return:
    '''
    if target.dict["status"]!=target.committed_state["status"] and target.dict["status"]=="pay_success":
        event.listen(target.session,"after_commit",pay_success_reminder2(target.dict["order_no"]) )

class Recharge(ModelBase):
    __tablename__ = 'recharge'
    __table_args__ = ()
    pass

class Gift(ModelBase):
    __tablename__ = 'gift'
    __table_args__ = ()
    pass

class AlipayInfo(ModelBase):
    __tablename__ = 'alipay_info'
    __table_args__ = ()
    pass

class InsteadRecharge(ModelBase):
    __tablename__ = 'instead_recharge'
    __table_args__ = ()
    pass

class WorkOrder(ModelBase):
    __tablename__ = 'workorder'
    __table_args__ = ()
    id=Column("workoder_id",Integer, primary_key=True,autoincrement=True)
    workorder_no=Column(String(32))
    workordertype=Column("workorder_type_id",Integer, ForeignKey('workorder_type.workorder_type_id'),nullable=False)
    apply_by=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    apply_source=Column(String(32))
    theme=Column(String(256))
    content=Column(String(4000))
    status=Column(String(32))
    apply_at=Column(DateTime, default=utcnow)
    lasthandled_at=Column(DateTime, onupdate=utcnow)
    lasthandled_by=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    records=relationship('WorkOrderRecord',order_by="desc(WorkOrderRecord.record_at)")
    type=relationship('WorkOrderType')

class WorkOrderRecord(ModelBase):
    __tablename__ = 'workorder_record'
    __table_args__ = ()
    id=Column("workorder_record_id",Integer, primary_key=True,autoincrement=True)
    workorder=Column("workorder_id",Integer, ForeignKey('workorder.workoder_id'),nullable=False)
    record_by=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    content=Column(String(4000))
    status=Column(String(32))
    record_at=Column(DateTime, default=utcnow)
    order=relationship("WorkOrder")

class WorkOrderType(ModelBase):
    __tablename__ = 'workorder_type'
    __table_args__ = ()
    id=Column("workorder_type_id",Integer, primary_key=True,autoincrement=True)
    name=Column(String(64))
    code=Column(String(32))
    remark=Column(String(256))
