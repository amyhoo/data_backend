# --*-- coding: utf-8 --*--
__author__ = 'yamin'
from oslo_config import cfg
CONF = cfg.CONF
if_email=[cfg.BoolOpt('if_email',default=True,help=''),]
if_sms=[cfg.BoolOpt('if_sms',default=False,help=''),]

email_user=[
    cfg.DictOpt('email_user',
                default={
                    "username":"",
                    "email":"",#邮件地址
                    "smtp_server":"",#邮件服务
                    "sign":"", #签名
                    "password":"",
                    "telephone":""
                },
                help=''),
    ]
CONF.register_opts(if_email)
CONF.register_opts(if_sms)
CONF.register_opts(email_user)