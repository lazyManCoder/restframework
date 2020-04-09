响应模块

响应头headers
响应体就是返回的内容
response = handler(request, *args, **kwargs)


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
	
	
	
响应类构造器
	class Response(SimpleTemplateResponse):
    """
    data:相应数据
	status:http响应状态吗
	template_name:drf渲染的页面模板
	headers:响应头
	exception:是否异常了
	content_type:响应的数据格式，响应头都带了，默认是json
    """

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

常规实例化对象
	from rest_framework.views import exception_handler as drf_excepion_handler
	from rest_framework.views import Response
	from rest_framework import status
	def exception_handler(exc, context):
		response = drf_excepion_handler(exc,context)
		if response is None:
			return Response({
				'detail':'error'
			},status=status.~,exception=True,headers={})
		return response
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	