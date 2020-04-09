# rest framework框架

普通开发

- 前后端放在一起写
- 前后端分离



后端开发

- 为前端提供url（API的开发/接口开发）
- 永远都是返回HttpResponse



Django FBV 、CBV

- function  base view
- class base view

```
views.StudentViews.as_view()

from django.views import View
class StudentViews(View):
	def get(self,request,*args,**kwargs):
		pass
	
	def post():
		pass
		
	def put():
		pass
		
	def delete():
		pass
```

postman可以伪造各种请求



列表生成式

- 



面向对象

- 封装
  - 对同一类方法封装到类中
  - 将数据封装到对象中



CBV 基于反射实现，根据请求方式不同，执行不同的方法

原理：

- 路由url -> view函数 -> dispatch方法(反射执行其他：/get/post/put/delete)

继承（多个类共用的功能，为了避免重复代码）

```
class MybaseView(object):
	def dispatch(self, request, *args, **kwargs):
        print('before')
        ret = super(StudentsView,self).dispatch(request, *args, **kwargs)
        print('after')
        return ret


class StudentsView(MybaseView,View):

    def dispatch(self, request, *args, **kwargs):
        print('before')
        ret = super(StudentsView,self).dispatch(request, *args, **kwargs)
        print('after')
        return ret

    def get(self,request,*args,**kwargs):
        return HttpResponse('get')

    def post(self,request,*args,**kwargs):
        return HttpResponse('post')

    def put(self,request,*args,**kwargs):
        return HttpResponse('put')
    def delete(self,request,*args,**kwargs):
        return HttpResponse('delete')

class TeachView(MybaseView,View): #多继承的的时候，在前面先放基础的

    def get(self,request,*args,**kwargs):
        return HttpResponse('get')

    def post(self,request,*args,**kwargs):
        return HttpResponse('post')

    def put(self,request,*args,**kwargs):
        return HttpResponse('put')
    def delete(self,request,*args,**kwargs):
        return HttpResponse('delete')

```



小知识点：

csrf是基于什么？

django中间件最多写多少方法？ 

最多五个

- process_request
- process_response
- process_view
- process_exception
- process_render_template

使用中间件做过什么？

- 权限
- 用户登录认证
- django的csrf是如何实现的？ csrf_token放在view中
  - process_request 检查视图是否被装饰
  - 去请求体获取cookie中获取token

```
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator

#方法一
class StudentsView(View):	
	@method_decorator(csrf_exempt) #类里面的方法名
	def dispatch(self, request, *args, **kwargs):
        return super(StudentsView,self).dispatch(request, *args, **kwargs)
        

    def get(self,request,*args,**kwargs):
        return HttpResponse('get')
	
	@method_decorator(csrf_exempt)  #加入到单独的方法中是无效的
    def post(self,request,*args,**kwargs):
        return HttpResponse('post')

    def put(self,request,*args,**kwargs):
        return HttpResponse('put')
    def delete(self,request,*args,**kwargs):
        return HttpResponse('delete')


#方法二
@method_decorator(csrf_exempt,name='dispatch')
class StudentsView(View):	
	@method_decorator(csrf_exempt) #类里面的方法名
	def dispatch(self, request, *args, **kwargs):
        return super(StudentsView,self).dispatch(request, *args, **kwargs)
        

    def get(self,request,*args,**kwargs):
        return HttpResponse('get')
	
	@method_decorator(csrf_exempt)  #加入到单独的方法中是无效的
    def post(self,request,*args,**kwargs):
        return HttpResponse('post')

    def put(self,request,*args,**kwargs):
        return HttpResponse('put')
    def delete(self,request,*args,**kwargs):
        return HttpResponse('delete')
```

总结：

- 本质：基于反射
- 流程：路由url -> view函数 -> dispatch方法(反射执行其他：/get/post/put/delete)
- 取消csrf认证要将装饰器装到dispatch方法上，且用method_decorator装饰

扩展：

- csrf
  - 基于中间件的process_view方法
  - 装饰器给单独函数设置认证或无认证





restful 规范（建议） https://www.cnblogs.com/wupeiqi/articles/7805382.html

1.对于一个订单写一个url，根绝method的不同进行区分

协议：

- API与用户的通信协议，总是使用HTTPS协议
- 域名
  - www.baidu.com
  - api.baidu.com
  - url方式
  - www.baidu.com/api
- 版本  https://api.baidu.com/v1/
- 面向资源编程   https://api.baidu.com/v1/名词/

method

- GET:从服务器取出资源
- POST：在服务器新建一个资源
- PUT：在服务器更新资源（客户端提供改变后的完整资源）
- PATCH：在服务器更新资源（客户端提供改变的属性）
- DELETE：从服务器删除资源

状态码

```
200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]：用户删除数据成功。
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。

return HttpResponse(,status=201)   改变状态吗
```



谈谈你对restful api 规范认识？

本质上就是一个规范，更容易处理，让URL体现出它的操作



## django rest framework

安装这个模块

```
pip install djangorestframework
```

CBV 执行dispatch

```
def get_parsers(self):
        """
        Instantiates and returns the list of parsers that this view can use.
        """
    return [parser() for parser in self.parser_classes]
        
 
```

使用很简单

源码流程



认证流程

1.找到APIView中的dispatch模块

```
def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """

        self.args = args
        self.kwargs = kwargs
        #对原生的request加工（丰富了一些功能）
        #Request(request,parsers=self.get_parsers(),authenticators=self.get_authenticators(),negotiator=self.get_content_negotiator(),# parser_context=parser_context
        #request(原生request,[BasicAuthentication对象，]
        #封装request
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?


        try:
            #认证
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)

            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        return self.response

```

分析：`request = self.initialize_request(request, *args, **kwargs)`  查看 `initialize_request`这个方法。这时候的self是，order这个对象

```
def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        parser_context = self.get_parser_context(request)

        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )
```

重新封装了request， `authenticators=self.get_authenticators(),` 

```
authentication_classes = [MyAuthentication,]
将要认证的类添加进来
def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        #类的实例化 order

        return [auth() for auth in self.authentication_classes]
```



继续往下找，到 `self.initial(request, *args, **kwargs)`

```
def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        #3.实现认证
        self.perform_authentication(request)

        self.check_permissions(request)
        self.check_throttles(request)
```

这一步 `self.perform_authentication(request)` 为了实现验证

```
def perform_authentication(self, request):
        """
        Perform authentication on the incoming request.

        Note that if you override this and simply 'pass', then authentication
        will instead be performed lazily, the first time either
        `request.user` or `request.auth` is accessed.
        """

        request.user
```



```
@property
    def user(self):
        """
        Returns the user associated with the current request, as authenticated
        by the authentication classes provided to the request.
        """

        if not hasattr(self, '_user'):
            with wrap_attributeerrors():
                #获取认证对象，进行一步步的认证
                self._authenticate()
        return self._user
```



django 请求声明周期

wsgi -> 中间件 -> 路由 -> 视图 -> dispatch方法进行调用



解析器：

request.post   request.body

允许用户发送JSON格式，也可以通过AJAX进行发送数据，

主要是解决，接受处理的问题

1.获取用户请求

2.获取用户请求体

3.根据用户请求头 和 parse_classes中支持的请求头进行比较

4.JSONParse对象去请求体

5.request.data



本质  源码  请求头  状态吗  请求方法

序列：

- 序列化处理
- 验证校验



## 分页

- 分页，看第几页，每页显示的n条数据
- 分页，在某个位置，向后查看多少条数据
- 加密分页，上一页和下一页。如果用了最后一个分页，很多数据速度也不会很慢
  - 反爬虫可以使用，这个url的页码是加密的  速度会得到控制

会有上下页码的url

``` 
return pg.get_paginated_response(ser.data)
```



```
offset = 0 索引
limit = 3 向后取三条数据
max_limit  设置最大的限制

```





视图

路由跟视图里面的类应该要联系一起用

