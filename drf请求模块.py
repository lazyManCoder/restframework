请求模块

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
	#封装request   请求模块
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
	
	
	
request = self.initialize_request(request, *args, **kwargs)
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
	

self.name:魔法方法(内置方法) 本质上走的是 self.__getattr__
def __getattr__(self, attr):
	
	"""
	self:request
	self.user
	request.META
	If an attribute does not exist on this instance, then we also attempt
	to proxy it to the underlying HttpRequest object.
	"""
	try:
		#兼容  先去原生（WSGI)的去找，拓展了reuqest的功能
		return getattr(self._request, attr)
	except AttributeError:
		#如果没哟找到就会到自身去找
		return self.__getattribute__(attr)
		
request.query_params  拓展性
POST请求有三种请求： JSON  
request.data  兼容性最强  三张数据方式都行，form_data json 

原生request对象的属性和方法都以直接被兼容
drf中所以的url参数都被解析到request.query_params   数据报都提交到 request.data

class Request:
    """
    Wrapper allowing to enhance a standard `HttpRequest` instance.

    Kwargs:
        - request(HttpRequest). The original request instance.
        - parsers_classes(list/tuple). The parsers to use for parsing the
          request content.
        - authentication_classes(list/tuple). The authentications used to try
          authenticating the request's user.
    """

    def __init__(self, request, parsers=None, authenticators=None,
                 negotiator=None, parser_context=None):
		
		#一定要遵循http协议
        assert isinstance(request, HttpRequest), (
            'The `request` argument must be an instance of '
            '`django.http.HttpRequest`, not `{}.{}`.'
            .format(request.__class__.__module__, request.__class__.__name__)
        )
		
		#二次封装request,将原生request作为drf request对象的_request属性
		#_request  内部使用
        self._request = request  #
        self.parsers = parsers or ()
        self.authenticators = authenticators or ()
        self.negotiator = negotiator or self._default_negotiator()
        self.parser_context = parser_context
        self._data = Empty
        self._files = Empty
        self._full_data = Empty
        self._content_type = Empty
        self._stream = Empty

        if self.parser_context is None:
            self.parser_context = {}
        self.parser_context['request'] = self
        self.parser_context['encoding'] = request.encoding or settings.DEFAULT_CHARSET

        force_user = getattr(request, '_force_auth_user', None)
        force_token = getattr(request, '_force_auth_token', None)
        if force_user is not None or force_token is not None:
            forced_auth = ForcedAuthentication(force_user, force_token)
            self.authenticators = (forced_auth,)

	
	
	
	
	
	
	
	
	
	