Cookie和session

Cookie

- 客户端浏览器上的一个文件

```rend
def login(requet):
    if y:
        res = redirect('/index') #后台的一个对象
        res.set_cookie('username',u) # 给后台的对象设置一个cookie
        return res
def index(requet):
	request.COOKIES.get('username')
	return render(requet,"index.html")
```





作页面的可以通过redirect返回到login页面，这样就可以确保数据的安全性



request请求所有东西

request.COOKIES  字典

request.COOKIES  ['username']

response = render()

response = redirect() 不仅返回内容，还要返回cookie

res.set_cookie('key',value)  关闭浏览器失效

```
res.set_cookie('key',value,max_age=10)  10s之后就会过期

import datetime
current_date = datetime.datetime.utcnow()
current_date = current_date + datetime.timedelta(seconds=10) 
res.set_cookie('key',value,expires=curremt_date)
res.set_cookie('key',value,httponly=true) 在js中无法获取到
只支持http传输

```

```
<script>
        $(function (){
            var v = $.cookie('per_page_count'，{'path':'/home/content.html/'}); 
            $('#t0').val(v);
        });

        function changePageSize(ths){
            var v = $(ths).val();
            console.log(v);
            $.cookie('per_page_count',v,{'path':'/home/content.html/'}); #这样写的话只有当前url生效
            location.reload()
        }
    </script>
```



带签名的cookie

```
加盐  密文的cookie
obj.set_signed_cookie('username','hanzi',salt="asdjhfja") #加密文
request.get_singned_cookie('username',salt="asdjhfja") #解密文

```





装饰器

FBV和CBV



用装饰器写用户认证

- FBV

```
def auth(func):
	def inner(request,*args,**kwargs):
		v = request.COOKIES.get('username1')
		if not v:
			return redirect('/login')
		return func(request,*args,**kwargs)
	return inner
```

- CBV

```
urls.py
path('Order/',views.Order.as_view())


from  django.utils.decorators import method_decorator
@method_decorator(auth,name='dispatch') #也可以这样写
class Order(views.View):
	@method_decorator(auth)
	def dispatch(self,request,*args,**kwargs):
		return super(Order,self).dispatch(request,*args,**kwargs)  #写了这一句下面就不用#auth

	def get(self,request):
		pass
	def post(self.requst):
		pass
	
```





session

基于cookie做验证：敏感信息放到cookie中别人可以看到

优点：将存储的数据压力放到本身电脑上

cookie 保存在用户浏览器中的键值对

session 保存在服务端的键值对

我们可以 把关于用户的数据保存在服务端，在客户端cookie里加一个sessionID（随机字符串）。其工作流程：

(1)、当用户来访问服务端时,服务端会生成一个随机字符串；

(2)、当用户登录成功后 把 {sessionID :随机字符串} 组织成键值对加到cookie里发送给用户；

(3)、服务器以发送给客户端 cookie中的随机字符串做键，用户信息做值，保存用户信息；

(4)、再访问服务时客户端会带上sessionid，服务器根据sessionid来确认用户是否访问过网站


```
if user == 'root' and pwd == '123':
	#生成随机字符串
	#写到用户浏览器cookie
	#保存到seesion
	#在随机字符串对应的字典中设置相关内容
request.session['username'] = user  #用seesion之前要执行表
request.session['is_login'] = True
默认保存在数据库中


def index(request):
#获取随机字符串
#根据字符串获取对应的信息
	if request.session['is_login']:
		return HttpResponse('ok')
	else:
		return
        
 依赖cookie
 
 request.session.get('k1',None)
 request.session.setdefault()
 
 
del request.session()
 request.session.delete("sesion_key") #删除所有信息
  request.session.clear()
	 
     
 request.session.session_key
 
  request.session.clear_expired()  将失效的日期的数据删除（脏数据）
   request.session.exsits("seesion_key") 验证一下
   
   
 在前端可以使用request.session.username 拿到用户
 
 def logout():
 	request.session.clear()
 	
 	
 request.session.set_expiry(value)  设置超时时间
 如果value = 0 用户关闭浏览器session就会失效
 如果value是none ，session会依赖全局seesion失效策略
 
 SESSION_SAVE_EVERY_REQUEST = False  是否每次请求都保存session
 
 session要依赖于cookie
 用户来请求，登陆成功后给他生成随机字符串，在服务器上也保存起来，并且在保存起来的这些字符串里面，它也能对应一个字典，这里面放置当前用户的所有信息，
 
 服务器session
 
 配置文件中设置默认操作
 SESSION_COOKIE_AGE = 1209600    session的失效日期（2周）默认
 
 
 
 
```

