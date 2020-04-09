[TOC]

# Django一些原理（中间件等）

## CSRF原理



看你后台发来的数据有没有随机字符串

全局发post请求 在form表中写 {{csrf_token}}  

```
{% csrf_token %}
```

如果别人的网站没有设置这个，我们可以通过自己的网站向网站中提交数据

做了一层防护



Ajax带什么  cookie里面也生成了

怎样通过ajax去发送

```
token = $.cookie('csrftoken')

发送ajax请求的实质
obj = XMLHttpRequest()
obj.open()
obj.send()   #ajax封装起来了

function csrfSafeMethod(method){
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({  #对页面中所有的ajax做操作 配置一遍
	beforeSend:function(xhr,setting){  #xml对象 jquery调用的就是XMLHttpRequest()这个对象
		if (!csrfSafeMethod(setting.type) && !this.crossDomain){  #做一个判断
			xhr.setRequestHeader('X-CSRFtoken'，token)	#设置请求头
		}
		
	}
})


$.ajax({
	url : '/login/',
	type:"POST",
	data:{'user':'root','pwd':'123'},
	success:function(arg){
		
	}
})
```

有两个form不用加csrf_token

```
from django.views.decorators.csrf import csrf_exempt,csrf_protect
@csrf_exempt
def index(request): #说明这个就不需要用csrf认证了

@csrf_protect
def index(): #单一的进行使用


```





## 中间件



![7b121dbd879580ce128723790b5ee66](C:\Users\BXYAPP~1\Local\Temp\WeChat Files\7b121dbd879580ce128723790b5ee66.png)



middleware

process_request   请求的经历

process_response

管道，请求穿过在穿回来

```
from django.utils.deprecation import MiddlewareMixin

class Row(MiddlewareMixin):
	def process_request(self,request):
		print('经过hello')
		
	def process_view(self,request,view_func,view_func_args,view_func_kwargs):
		print('jj')  #view里面的参数                tets(\d+)   test<?()>
	
	def process_response(self,request,response):
		return response

class Row1(MiddlewareMixin):
	def process_request(self,request):
		print('经过hello')
		
	def process_response(self,request,response):
		return response
	
加入到中间件
Middle.m1.Row1

做一个黑名单进行设置，就是一个普通的类，可以获取请求的ip进行限制

先穿过proce_request   进行路由映射匹配
这会之后在请求process_view
会触发process_exception  处理之后会返回response
没报错在返回process_response  

process_exception(self.request,exception):
	print('error')  #如果view里面出错就会执行这个
	if isinstance(exception,ValueError):
		reutrn HttpResponse()
		
process_template_response(self,request,response):
	#如果view中，返回对象，具有render方法
可以在view中这样写
class Foo:
	def render(self):
		return HttpResponse('render')

def test(request):
	return Foo()
```



## 缓存

请求第一次到数据库中拿取

下次直接去缓存中去拿

- 开发调式
- 内存
- 文件

```
# 此缓存将内容保存至文件
    # 配置：

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': os.path.join(BASE_DIR,'cache')
            }
        }
    # 注：其他配置同开发调试版本
    
    #test  对单独函数做缓存
    from django.views.decorators.cache import cache_page
    @cache_page(60 * 15)  #里面是失效实现（秒）
    def cache(request):
    	import time
    	ctime = time.time()
    	return render(request,'cache.html',{'ctime':ctime})   #基于视图做缓存
    	
    
    
    使用中间件，经过一系列的认证等操作，如果内容在缓存中存在，则使用FetchFromCacheMiddleware获取内容并返回给用户，当返回给用户之前，判断缓存中是否已经存在，如果不存在则UpdateCacheMiddleware会将缓存保存至缓存，从而实现全站缓存

    MIDDLEWARE = [
        'django.middleware.cache.UpdateCacheMiddleware', #将缓存返回到缓存的地方
        # 其他中间件...
        'django.middleware.cache.FetchFromCacheMiddleware', #判断缓存中是否有数据，如果没有则继续下一级
    ]  #基于全局做缓存

    CACHE_MIDDLEWARE_ALIAS = ""
    CACHE_MIDDLEWARE_SECONDS = ""
    CACHE_MIDDLEWARE_KEY_PREFIX = ""
    
    {%load cache%}
    {{ctime}}  #具有模板做缓存
    {% cache 500 c1(缓存key) %} #500就是缓存的超时时间
    {{ctime}}  #不变我想作为缓存，单独做缓存
    {% endcache %}
```



- 数据库

```
# 此缓存将内容保存至数据库

    # 配置：
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'my_cache_table', # 数据库表
            }
        }

    # 注：执行创建表命令 python manage.py createcachetable
```



- Memcache缓存（python-memcached模块）

```
 CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                ('172.19.26.240:11211',10),
                ('172.19.26.242:11211',15), #权重   将列表弄成25 命中这台的几率高
            ]
        }
```



- Memcache缓存（pylibmc模块）



## 信号

Django在内部放了很多钩子，更有利于我们执行代码

- 内置信号

```
Model signals
    pre_init                    # django的modal执行其构造方法前，自动触发
    post_init                   # django的modal执行其构造方法后，自动触发
    pre_save                    # django的modal对象保存前，自动触发
    post_save                   # django的modal对象保存后，自动触发
    pre_delete                  # django的modal对象删除前，自动触发
    post_delete                 # django的modal对象删除后，自动触发
    m2m_changed                 # django的modal中使用m2m字段操作第三张表（add,remove,clear）前后，自动触发
    class_prepared              # 程序启动时，检测已注册的app中modal类，对于每一个类，自动触发
Management signals
    pre_migrate                 # 执行migrate命令前，自动触发
    post_migrate                # 执行migrate命令后，自动触发
Request/response signals
    request_started             # 请求到来前，自动触发
    request_finished            # 请求结束后，自动触发
    got_request_exception       # 请求异常后，自动触发
Test signals
    setting_changed             # 使用test测试修改配置文件时，自动触发
    template_rendered           # 使用test测试渲染模板时，自动触发
Database Wrappers
    connection_created          # 创建数据库连接时，自动触发
```

导入

```
from django.core.signals import request_finished
    from django.core.signals import request_started
    from django.core.signals import got_request_exception

    from django.db.models.signals import class_prepared
    from django.db.models.signals import pre_init, post_init
    from django.db.models.signals import pre_save, post_save
    from django.db.models.signals import pre_delete, post_delete
    from django.db.models.signals import m2m_changed
    from django.db.models.signals import pre_migrate, post_migrate

    from django.test.signals import setting_changed
    from django.test.signals import template_rendered

    from django.db.backends.signals import connection_created


    def callback(sender, **kwargs):  #sender一个参数
        print("xxoo_callback")
        print(sender,kwargs)

    xxoo.connect(callback)
    # xxoo指上述导入的内容   可以导入多个信号
```

单独创建一个sg.py放置起来

在__init__下导入sg

```
import sg  这样自动会加载到内存中去
```

自定义信号

- 创建一个信号

```
import django.dispatch
pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"]) #触发最少传递两个值
```



- 注册信号

```
def callback(sender, **kwargs):
    print("callback")
    print(sender,kwargs)
 
pizza_done.connect(callback)
```



- 触发信号

```
from 路径 import pizza_done
from sg import 
 
pizza_done.send(sender='seven',toppings=123, size=456) #sender:谁发送的，后面参数随意写
```



可以做一些邮件系统的通知  操作数据库之后的提醒



