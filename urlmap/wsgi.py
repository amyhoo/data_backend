__author__ = 'yamin'
import eventlet
import greenlet
from eventlet import wsgi
application=None#入口
server_params={
            'sock': "",#socket对象
            'site':application, #web服务器处理的应用
            'protocol': "",#处理协议,
            'max_size':"",#最多greenlet的个数
            'custom_pool':"",#greenlet个数
            'log': "",#log位置
            'log_output':"",#是否log
            'log_format': "",#格式化
            'debug': False,#是否开启debug模式，比如服务器500的时候，是否显示trace back 信息
            'url_length_limit':"",#URL的最大长度
            'keepalive':"" ,#为false的时候，如果响应了一个请求则关闭连接
            'socket_timeout': ""#为None的时候则永远等待
}
wsgi_server=eventlet.wsgi.server(**server_params)