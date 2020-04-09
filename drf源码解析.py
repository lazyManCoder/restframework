
urls.py
	from django.contrib import admin
	from django.urls import path,include,re_path
	from . import views
	app_name = 'api'
	urlpatterns = [
		path('admin/', admin.site.urls),
		re_path('^user',views.UsersView.as_view()),
	]

views.py
	from django.shortcuts import render,HttpResponse
	class UsersView():
		def get(self,request,*args,**kwargs):
			return HttpResponse('hello')

解析的是as_view这个方法
调用dispatch方法

class View:
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classonlymethod  #classonlymethodz作用:只能被类调用，不能被实例对象调用。
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:  # initkwargs
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))
		#上面在做的是异常处理
        def view(request, *args, **kwargs):

            self = cls(**initkwargs)  #实例化的对象  self = UsersView()
			#到self这个UsersView实例化的对象中找，方法
            if hasattr(self, 'get') and not hasattr(self, 'head'): 
                self.head = self.get
            self.setup(request, *args, **kwargs)
            if not hasattr(self, 'request'):
                raise AttributeError(
                    "%s instance has no 'request' attribute. Did you override "
                    "setup() and forget to call super()?" % cls.__name__
                )
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view
	
	#想当与做了一个初始化
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            'Method Not Allowed (%s): %s', request.method, request.path,
            extra={'status_code': 405, 'request': request}
        )
        return HttpResponseNotAllowed(self._allowed_methods())

    def options(self, request, *args, **kwargs):
        """Handle responding to requests for the OPTIONS HTTP verb."""
        response = HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response

    def _allowed_methods(self):
		# m = [] 
		# for m in self.http_method_names:
			# if hasattr(self,m):
				# m.append(m)
		# m.upper()
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
		

当然我们可以自定义dispatch方法

views.py
	from django.shortcuts import render,HttpResponse
	class UsersView(View):
		def dispatch(self,request,*args,**kwargs):
			print('hi')
			ret = super(UsersView,self).dispatch(request,*agrs,**kwargs) #HttpResponse('hello')
			print('after')
			return ret
			
		def get(self,request,*args,**kwargs):
			return HttpResponse('hello')
			
	
	from django.shortcuts import render,HttpResponse
	class MyBaseView:
		def dispatch(self,request,*args,**kwargs):  
			print('hi')
			ret = super(MyBaseView,self).dispatch(request,*agrs,**kwargs) #HttpResponse('hello')
			print('after')
			return ret
			
	class UsersView(MyBaseView,View):  #多继承的时候左边优先
		def get(self,request,*args,**kwargs):
			return HttpResponse('hello')
			

csrf是怎样验证：
	@csrf_exempt   不需要通过验证就可以  dispatch = csrf_exempt(dispatch)
	先判断函数有没有带装饰器，在查看token是否一致 process_view   
	判断是否带有随机字符串
def process_view(self, request, callback, callback_args, callback_kwargs):
	if getattr(request, 'csrf_processing_done', False):
		return None

	# Wait until request.META["CSRF_COOKIE"] has been manipulated before
	# bailing out, so that get_token still works
	if getattr(callback, 'csrf_exempt', False):
		return None

	# Assume that anything not defined as 'safe' by RFC7231 needs protection
	if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
		if getattr(request, '_dont_enforce_csrf_checks', False):
			# Mechanism to turn off CSRF checks for test suite.
			# It comes after the creation of CSRF cookies, so that
			# everything else continues to work exactly the same
			# (e.g. cookies are sent, etc.), but before any
			# branches that call reject().
			return self._accept(request)

		if request.is_secure():
			# Suppose user visits http://example.com/
			# An active network attacker (man-in-the-middle, MITM) sends a
			# POST form that targets https://example.com/detonate-bomb/ and
			# submits it via JavaScript.
			#
			# The attacker will need to provide a CSRF cookie and token, but
			# that's no problem for a MITM and the session-independent
			# secret we're using. So the MITM can circumvent the CSRF
			# protection. This is true for any HTTP connection, but anyone
			# using HTTPS expects better! For this reason, for
			# https://example.com/ we need additional protection that treats
			# http://example.com/ as completely untrusted. Under HTTPS,
			# Barth et al. found that the Referer header is missing for
			# same-domain requests in only about 0.2% of cases or less, so
			# we can use strict Referer checking.
			referer = request.META.get('HTTP_REFERER')
			if referer is None:
				return self._reject(request, REASON_NO_REFERER)

			referer = urlparse(referer)

			# Make sure we have a valid URL for Referer.
			if '' in (referer.scheme, referer.netloc):
				return self._reject(request, REASON_MALFORMED_REFERER)

			# Ensure that our Referer is also secure.
			if referer.scheme != 'https':
				return self._reject(request, REASON_INSECURE_REFERER)

			# If there isn't a CSRF_COOKIE_DOMAIN, require an exact match
			# match on host:port. If not, obey the cookie rules (or those
			# for the session cookie, if CSRF_USE_SESSIONS).
			good_referer = (
				settings.SESSION_COOKIE_DOMAIN
				if settings.CSRF_USE_SESSIONS
				else settings.CSRF_COOKIE_DOMAIN
			)
			if good_referer is not None:
				server_port = request.get_port()
				if server_port not in ('443', '80'):
					good_referer = '%s:%s' % (good_referer, server_port)
			else:
				try:
					# request.get_host() includes the port.
					good_referer = request.get_host()
				except DisallowedHost:
					pass

			# Create a list of all acceptable HTTP referers, including the
			# current host if it's permitted by ALLOWED_HOSTS.
			good_hosts = list(settings.CSRF_TRUSTED_ORIGINS)
			if good_referer is not None:
				good_hosts.append(good_referer)

			if not any(is_same_domain(referer.netloc, host) for host in good_hosts):
				reason = REASON_BAD_REFERER % referer.geturl()
				return self._reject(request, reason)

		csrf_token = request.META.get('CSRF_COOKIE')
		if csrf_token is None:
			# No CSRF cookie. For POST requests, we insist on a CSRF cookie,
			# and in this way we can avoid all CSRF attacks, including login
			# CSRF.
			return self._reject(request, REASON_NO_CSRF_COOKIE)

		# Check non-cookie token for match.
		request_csrf_token = ""
		if request.method == "POST":
			try:
				request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
			except IOError:
				# Handle a broken connection before we've completed reading
				# the POST data. process_view shouldn't raise any
				# exceptions, so we'll ignore and serve the user a 403
				# (assuming they're still listening, which they probably
				# aren't because of the error).
				pass

		if request_csrf_token == "":
			# Fall back to X-CSRFToken, to make things easier for AJAX,
			# and possible for PUT/DELETE.
			request_csrf_token = request.META.get(settings.CSRF_HEADER_NAME, '')

		request_csrf_token = _sanitize_token(request_csrf_token)
		if not _compare_salted_tokens(request_csrf_token, csrf_token):
			return self._reject(request, REASON_BAD_TOKEN)

	return self._accept(request)

	加入到中间件，就是全局使用，如果注释，还想用就得加上 @csrf_protect

	在CBV加上装饰器@csrf_protect就应该夹到
	from django.utils.decorators import method_decorator  #必须要加入到dispatch
	class UsersView(MyBaseView,View):
		@method_decorator(csrf_protect)   #这样就可以添加局部添加csrf验证了
		def dispatch(self,request,*args,**kwargs):
			return super(UsersView,self).dispatch(self,request,*args,**kwargs)
		
		def get(self,request,*args,**kwargs):
			return HttpResponse('hello')
			
		def get(self,request,*args,**kwargs):
			return HttpResponse('hello')
			
	如果不写dispatch，可以装修类
	@method_decorator(csrf_protect,name='dispatch')  #name就是找到里面的方法名
	class UsersView(MyBaseView,View):





接口
	联系两个物质的媒介，完成信息的交互，在WEB程序中；联系前台页面与后台数据库中的媒介
	url，爬虫所爬取的json就是接口的api

https://www.cnblogs.com/wupeiqi/articles/7805382.html
restful规范（建议）
	为了采用不同的后台语言，也能使用同样的接口获取到同样的数据
	如何写接口、写接口文档
	在URL中更好的体现出它的操作，交给前端
	
什么是RESTful
	REST与技术无关，代表的是一种软件架构风格，表征状态转移
	所有的数据，不过是通过网络获取的，还是操作的数据，都是资源，将一切数据视为资源
	对于REST这种面相资源的架构风格，有人提出一种全新的结构理念，面相资源架构（ROA）
	
RESTful API设计规范
	1.API与用户的通信协议，总是使用HTTPS协议
	2.域名
		https://api.example.com/  尽量将API部署在专用域名
		https://example.org/api/  API很简单
	3.版本
		URL : https://example.org/api/V1
		
	4.路径，视网络上任何东西都是资源，均使用名词表示
		https://example.org/api/zoos
		https://example.org/api/animals
	
	5.method
		GET    从服务器取出资源
		POST   在服务器新建一个资源
		PUT    在服务器更新资源（客户端提供改变后的完整资源）
		PATCH  在数据库更新部分资源
		DELETE 从服务器上删除资源
		
	6.过滤
		https://api.example.com/v1/zoos?limit=10：指定返回记录的数量
		https://api.example.com/v1/zoos?offset=10：指定返回记录的开始位置
		https://api.example.com/v1/zoos?page=2&per_page=100：指定第几页，以及每页的记录数
		https://api.example.com/v1/zoos?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序
		https://api.example.com/v1/zoos?animal_type_id=1：指定筛选条件

	7.装态码
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

	8.错误处理，状态码是4xx 应返回错误信息，error当作key
		{
			error:"Invalid API key"
		}
	
	9.返回结果，针对不同的操作，服务器向用户返回的结果应该符合下面的规范
		GET /collection：返回资源对象的列表（数组）
		GET /collection/resource：返回单个资源对象
		POST /collection：返回新生成的资源对象
		PUT /collection/resource：返回完整的资源对象
		PATCH /collection/resource：返回完整的资源对象
		DELETE /collection/resource：返回一个空文档

	10.Hypermedia API ,RESTful API最好做到Hypermedia，即返回结果中提供链接，连向其他API方法，使得用户不查文档，也知道下一步应该做什么。
		{"link": {
		  "rel":   "collection https://www.example.com/zoos",
		  "href":  "https://api.example.com/zoos",
		  "title": "List of zoos",
		  "type":  "application/vnd.yourformat+json"
		}}
		

drf框架
	pip install djangorestframework
	
	from rest_framework.views import APIView
	class APIView(View):
		pass
	
	class Order(APIView):
		pass  #这个类中的功能更多
		
认证组件
APIView中的dispatch
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

def initialize_request(self, request, *args, **kwargs):
	"""
	Returns the initial request object.
	"""
	#准备要解析的数据
	parser_context = self.get_parser_context(request)

	return Request(
		request, #原生的
		#获取解析类
		parsers=self.get_parsers(),
		authenticators=self.get_authenticators(), #要先从UserView中查找
		negotiator=self.get_content_negotiator(),
		parser_context=parser_context
	)
	
	
	

def get_authenticators(self):
	"""
	Instantiates(实例化) and returns the list of authenticators(验证器) that this view can use.
	"""
	#类的实例化 order
	# auth = []
	# for auth in self.authentication_classes:  #读的是配置文件，如果在类中写，就使用自己的
		# auth.append(auth)
	# auth()  实例化的对象 
	return [auth() for auth in self.authentication_classes]


self.initial(request, *args, **kwargs)
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

self.perform_authentication(request)
def perform_authentication(self, request):
	"""
	Perform authentication on the incoming request.

	Note that if you override this and simply 'pass', then authentication
	will instead be performed lazily, the first time either
	`request.user` or `request.auth` is accessed.
	"""

	request.user

在去找request
from rest_framework.request import Request
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


self._authenticate()
def _authenticate(self):
	"""
	Attempt to authenticate the request using each authentication instance
	in turn.
	"""
	#循环所有的认证对象   MyAuthentication  
	for authenticator in self.authenticators: #self.authenticators = authenticators or ()
		try:
			user_auth_tuple = authenticator.authenticate(self) #返回一个元组

		except exceptions.APIException:
			self._not_authenticated()
			raise

		if user_auth_tuple is not None:
			self._authenticator = authenticator
			self.user, self.auth = user_auth_tuple
			return

	self._not_authenticated()





from rest_framework.authention import BasicAuthentication
from django.shortcuts import render,HttpResponse

class MyAuthentication:
	def authenticate(self,request):
		token = request._request.GET.get('token')
		if not token:
			raise exceptions.AuthenticationFailed('用户认证失败')
		
		return ('bob',None)

class UsersView(APIView):
	authentication_classes = [MyAuthentication,]
	def get(self,request,*args,**kwargs):
		return HttpResponse('hello')


class BaseAuthentication:
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass
		
class BasicAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        userid, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(userid, password, request)

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm




执行request.query_params  == request._request.GET
@property
def query_params(self):
	"""
	More semantically correct name for request.GET.
	"""

	return self._request.GET

六大基础接口
	获取 增加 删除 整体 局部
十大接口 
	群增 群删 整体修改 局部修改



			

