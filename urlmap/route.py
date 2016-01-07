import routes
import webob

class BaseMapper(routes.Mapper):
    '''
    '''
    def routematch(self, url=None, environ=None):
        '''
        对某些route可以特殊处理
        '''
        return routes.Mapper.routematch(self, url, environ)

    def connect(self, *args, **kargs):
        '''
        设置参数
        '''
        return routes.Mapper.connect(self, *args, **kargs)

    def resource(self, member_name, collection_name, **kwargs):
        '''
        条目太多进行简化
        member_name,路由名字
        collection_name:路由名字复数
        '''
        routes.Mapper.resource(self, member_name,collection_name,**kwargs)

class BaseRouter(object):
    '''
    通用的url路由器
    '''
    def set_route(self):
        raise NotImplementedError()

    def __init__(self):
        self._mapper = routes.Mapper()#
        self.set_route()
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, self._mapper)

    @webob.dec.wsgify
    def __call__(self, req):
        return self._router

    @staticmethod
    @webob.dec.wsgify()
    def _dispatch(req):
        match = req.environ['wsgiorg.routing_args'][1] #RoutesMiddleware设置
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller'] #app即为self._mapper.connect 设置的controller
        return app