[TOC]



# Django restframework异常处理模块解析





## 主要的作用：

- 处理我们逻辑异常，只要是通过路由进入我们的视图中的错误，都可以实现自定制的报错。
- 例如，`http://127.0.0.1:8000/api/v1/use/10/` 后面的10就是我们在业务逻辑代码所要取的第几条数据，但是我们的数据库中少于10条数据，那么页面就会产生报错，会出现404的报错，这是`exception_handler`这个句柄函数中默认处理的功能。

## 实现方法

我们通过具体的实例进行解析：

urls.py

```
urlpatterns = [
    re_path('^(?P<version>[v1|v2]+)/use/$', views.UseView.as_view()),
    re_path('^(?P<version>[v1|v2]+)/use/(?P<pk>\d+)/$', views.UseView.as_view()),
]
```



models.py

```
from django.db import models

# Create your models here.
class User(models.Model):
    SEX = (
        (1,'男'),
        (2,'女'),
    )
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    sex = models.IntegerField(choices=SEX)
    icon = models.ImageField(upload_to='icon',default='icon/2.jpg')

    class Meta:
        db_table = 'usersex'
        verbose_name = '信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<<%s>>' % self.name
```



views.py

```
from rest_framework.views import APIView
from rest_framework.response import Response

class UseView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            user_obj = models.User.objects.get(pk=pk)
            user_ser = serializser.UserSerializser(user_obj)
            return Response({
                'status':0,
                'msg':0,
                'results':user_ser.data
            })
        else:
            user_obj_list = models.User.objects.all()
            user_ser_list = serializser.UserSerializser(instance=user_obj_list,many=True) 
            print(user_ser_list)
            return Response({
                    'status':0,
                    'msg':0,
                    'results':user_ser_list.data
                })

```

settings.py

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.exception.exception.exception_handler',
}
```

`api.exception.exception.exception_handler`我们自定义exception_handler的路径

```
# author navigator
from rest_framework.views import exception_handler as drf_excepion_handler
from rest_framework.views import Response
def exception_handler(exc, context):
	response = drf_excepion_handler(exc,context)
	if response is None:
		ret = "%s-%s-%s"%(context["view"],context["request"].method,exc)
		return Response({ 
			'detail':ret
			})
	return response
```



上面的代码，一旦 `url` 中 `pk` 超出我们数据库中的值,就会自动触发我们自己设置的句柄

```
{
    "detail": "<api.views.UseView object at 0x000001D46254EBE0>-GET-User matching query does not exist."
}
```



如果只是想要设置全局的报错这些应该就足够。

## 源码解析

下面分析下源码

首先请求会触发到 `APIView` 中的 `dispatch`方法

```
def dispatch(self, request, *args, **kwargs):
        。。。

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        return self.response
```

当三大认证中出现报错，将会触发异常，所以我们应该关注 `response = self.handle_exception(exc)`

首先我们在 我们自己的类 `UseView` 去找有没有 `handle_exception` 这个方法，如果没有我们就到 `APIView`中去查询。没有我们再去它的爷爷类 `View`找

```
def handle_exception(self, exc):
	"""
	Handle any exception that occurs, by returning an appropriate response,
	or re-raising the error.
	"""
	#做一个类型的判断，看看是否是因为没有认证或者是因为认证失败产生的异常
	if isinstance(exc, (exceptions.NotAuthenticated,
						exceptions.AuthenticationFailed)):
		# WWW-Authenticate header for 401 responses, else coerce to 403
		auth_header = self.get_authenticate_header(self.request)

		if auth_header:
			exc.auth_header = auth_header
		else:
			exc.status_code = status.HTTP_403_FORBIDDEN
	
	#判断之后，便会执行这句话，我们可以根据这个  get_exception_handler 方法继续查看
	#获取异常处理的方法
	exception_handler = self.get_exception_handler()
	context = self.get_exception_handler_context()
	
	#异常处理的结果
	response = exception_handler(exc, context)
	
	#如果不是以上捕捉的异常，则会按照restframework中自定义的处理，所以我们要处理的也是这个
	if response is None:
		self.raise_uncaught_exception(exc)

	response.exception = True
	return response
```



`get_exception_handler()`

```
def get_exception_handler(self):
	"""
	Returns the exception handler that this view uses.
	"""
	return self.settings.EXCEPTION_HANDLER
```



这个返回的就是全局配置，此时的 `self` 是`views`,所以我们可以进入到 `rest_framework` 中的 `setting.py` 去查找这个字段

```
#这个里面我们，可以找到它的配置路径，所以，我们可以通过该配置路径，实现自定义的exception_handler
'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
'NON_FIELD_ERRORS_KEY': 'non_field_errors',
```



在 `restframework/views.py`找到 `exception_handler`的方法

```
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

    return None

```



`exc`就是具体的报错信息

context`就是初始化了下面的参数，所以通过字典的取值可以查看详细的参数。

```
def get_exception_handler_context(self):
        """
        Returns a dict that is passed through to EXCEPTION_HANDLER,
        as the `context` argument.
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None)
        }
```



以上就是一场模块的流程，可以通过 `pycharm`中的断点调试，一步步的进行理解。

有了这个模块，那没有处理的异常，就会得到处理，让前端得到合理的异常信息。



好啦，今天就到这了，理解尚浅，不断查看源码，希望会有更深的理解，加油！

