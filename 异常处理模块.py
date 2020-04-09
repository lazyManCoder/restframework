异常处理模块
用get进行异常

pk = kwargs.get('pk')


异常处理模块的入口
except Exception as exc:
	response = self.handle_exception(exc)
	
def handle_exception(self, exc):
	"""
	Handle any exception that occurs, by returning an appropriate response,
	or re-raising the error.
	"""
	#类型判断   没有认证或者认证报错
	if isinstance(exc, (exceptions.NotAuthenticated,
						exceptions.AuthenticationFailed)):
		# WWW-Authenticate header for 401 responses, else coerce to 403
		auth_header = self.get_authenticate_header(self.request)

		if auth_header:
			exc.auth_header = auth_header
		else:
			exc.status_code = status.HTTP_403_FORBIDDEN
	
	#句柄  ：句柄是一个标识符，是拿来标识对象或者项目的  相当于工具 logger  完成最终的统筹规划
	#获取异常处理的方法（句柄）
	exception_handler = self.get_exception_handler()

	context = self.get_exception_handler_context()
	#异常处理的结果
	response = exception_handler(exc, context)
	异常结果为空，就会抛出异常
	#
	if response is None:
		#没有异常信息，抛出异常
		self.raise_uncaught_exception(exc)
	
	#有异常内容，返回异常内容
	response.exception = True
	return response

#没有异常信息，抛出异常  直接到中间件中去修改内容
def raise_uncaught_exception(self, exc):
	if settings.DEBUG:
		request = self.request
		renderer_format = getattr(request.accepted_renderer, 'format')
		use_plaintext_traceback = renderer_format not in ('html', 'api', 'admin')
		request.force_plaintext_errors(use_plaintext_traceback)
	raise exc

def get_exception_handler(self):
	"""
	Returns the exception handler that this view uses.
	"""
	return self.settings.EXCEPTION_HANDLER  #在API中直接设置  只要出现这样的内容我们都可以进行自定义的配置
	
	
去API settings中去找
# Exception handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',
	
exc则是报错的异常
from rest_framework.views import exception_handler
def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
	#如果没有就返回None，其他的异常，中间件处理的我们课以进行转换
    return None

如果我们自定义处理的话，我们就可以自己写这个方法
在全局中修改异常的路径
REST_FRAMEWORK = {
    #'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
	'EXCEPTION_HANDLER': 'api.exception.exception_handler', 
}

新建一个exception
from rest_framework.views import exception_handler as drf_excepion_handler
from rest_framework.views import Response
def exception_handler(exc, context):
	response = drf_excepion_handler(exc,context)
	if response is None:
		return Response({  #通过context exc记录详细的异常
			'detail':'error'
			})
	return response



为什么要自定义异常模块
	1.所有经过drf的APIView视图类产生的异常，都可以提供异常处理方案
	2.drf默认提供了异常处理方案（rest_framework.views.exception_handler)
	但是处理范围有限
	3.drf提供的处理方案两种，处理了返回异常，没处理返回None，接着后续服务器
	抛异常给前台
	4.自定义异常的目的就是解决没有处理的异常，让前台得到合理的异常信息返回，后天记录异常具体信息
	

status可以使用网络状态吗





def http_method_not_allowed(self, request, *args, **kwargs):
	"""
	If `request.method` does not correspond to a handler method,
	determine what kind of exception to raise.
	"""
	raise exceptions.MethodNotAllowed(request.method)
	
class MethodNotAllowed(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = _('Method "{method}" not allowed.')
    default_code = 'method_not_allowed'

    def __init__(self, method, detail=None, code=None):
        if detail is None:
            detail = force_str(self.default_detail).format(method=method)
        super().__init__(detail, code)
		
404错误的时候，在中间件中，在执行视图函数抛出错误

404因为没有404这个路由，所以我们可以得知这个事情是在中间件中进行处理的结果
只要是走逻辑异常，进入路由之后，就可以实现这个方法

