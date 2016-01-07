__author__ = 'yamin'
from .route import BaseRouter

class Router(BaseRouter):
    def set_route(self):
        from controller.workorder import Controller as workorder_controller
        self._mapper.connect('workorder/create',controller=workorder_controller,#设置响应程序
         action='create_workorder',conditions={'method': ['POST']})#注册一条路由