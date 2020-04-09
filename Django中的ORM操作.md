# Django中的ORM操作



层层深入，了解Django的MTV模式

- Model(模型)：负责业务对象与数据库对象（ORM）
- Template(模板)：负责如何把页面展示给用户
- View(视图)：负责业务逻辑，用于调用Model和Template

![](https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1405962861,590806281&fm=26&gp=0.jpg)

我们今天所要介绍的就是ORM操作

什么是ORM？

ORM，即Object-Relational Mapping（对象关系映射），它的作用是在关系型数据库和业务实体对象之间作一个映射，当我们在具体的操作业务对象的时候，不需要再去和复杂的SQL语句打交道，只需简单的操作对象的属性和方法。





![](https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1347702149,2377690075&fm=26&gp=0.jpg)



什么是持久化？

![](https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1793465997,498067778&fm=26&gp=0.jpg)



DB first / code first

- first 手动创建数据库以及表  ->  ORM框架  ->  自动生成类
- code 手动创建类和数据库   ->   ORM框架  ->  自动生成表



ORM的增删改查

```
models.UserInfo.objects.create() #增

res = models.UserInfo.objects.all() #返回所有的数据 QuerySet类 像列表
print(res.query) 当前的sql语句

models.UserInfo.objects.filter() #查 
models.UserInfo.objects.filter().first() # 拿第一个元素
models.UserInfo.objects.get() # 可以查询第一条语句，但是如果没有数据将会报错 使用前应该try
models.UserInfo.objects.filter().count()  #查询个数

models.UserInfo.objects.all().delete()

models.UserInfo.objects.all.update(pwd=88) #更新，将所有的密码都变为88



```



要善于使用正则，来判断页面的数据，比如博客，这样就可以在数据库中进行查询到详细的信息

使用正则表达式必须使用re_path

null=True  可以为空

models的字段

models.EmailField  在admin做一些认证

AutoField(primary_key=True)  自增列

创建一个超级用户：python mangae.py createsuperuser

root



字段的参数

	null   -->创建数据库的时候是否为空
			default   -->默认值
			primary_key   -->主键
			db_column   -->修改列名   password = models.CharField(max_length=63,db_column='pwd')
			db_idnex    -->是否索引   unique=True    db_idnex=True
			unique      -->唯一索引
			unique_for_date  --> 只对日期做索引
			unique_for_month
			unique_for_year
			auto_now   ->创建时，自动生成
			auto_now_add
			choice -> 吧选项放入内存中  django admin 显示下拉框   避免连表查询
			blank -> django admin 是否可以为空   blank=True 可以为空
			verbose_name -> django admin  verbose_name='用户名'  显示中文
			editable -> django admin  控制是否可以被编辑
			error_messages -> django admin error_messages={'required':'请输入密码'}
			help_text -> django admin 提示
			validators -> django admin 自定义错误信息

ctime = models.DateTimeField(auto_now_add=True)  自动加入创建的当前时间

uptime = models.DateTimeFiled(auto_now=True,null=True)

更新的条件应该是通过

obj = models.unu.objects.filter(id=1).first()

obj.caption = "CEO"

obj.save() 这总方式才可以进行更新





choice  将数据放到内存中  在admin中显示下拉框  连表查询效率低

```。
user_type_choices = (
	(1,'超级用户'),
	(2,'普通用户'),
	(3,'游客'),
)
user_type_id = models.IntegerFiled(choices=user_type_choices)
```





ORM外键操作

user_group = models.Foregin()



for row in user_list:

​	print(row.user_group_id)  #就是分组的具体数  跨表查询

```
class Content(models.Model):

    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    crate_time = models.DateTimeField(auto_now_add=True,unique_for_month=True)
    update_time = models.DateTimeField(auto_now=True)
```

​	print(row.user_group)  #就是一个对象  代指封装外键中的对象

​	print(row.user_group.uid)

 

django.db.utils.IntegrityError: UNIQUE constraint failed: new__home_content.nid



```
class UserInfo(models.Model):    user = models.CharField(max_length=32)    pwd = models.CharField(max_length=32)    
```

要在路由上加终止符 $

bussiness$/

bussiness_add /  如果上面不加终止符，那么下面的url永远不会执行

models.Bussiness.objects.filter(nid__gt=0)    上面中的内部类型都是对象

v1 = models.Bussiness.objects.all()  #内部是对象

v2 = models.Bussiness.objects.all().values("id","caption") === select id ,caption from Bussion

[{'id':1,'caption':'运维部'},{},{}]



v3 = models.Bussiness.objects.all().values_list("id","caption")

[(1,运维部)，（2，开发)]   元组

z只能用索引  row.0 在模板语言





{{ forloop.counter }}  计数器

{{ forloop.reversecount(0) }} 从0倒序



v2 = models.Bussiness.objects.filter().values("id","caption","b_id","b__caption")   跨表操作

filter().values("id","caption","b_id","b__caption")   跨表就是双下滑线



业务线名称

```
{% for op in b_list %}
<option value="{{op.id}}">{{op.caption}}</option>
{% endfor %}

data = $('#add_modal').serialize()  将form中的值全部都发送给后台
success:function(data){
	
}


r = models.ManyToManyFiled("host")
obj.r.add()  r外键  对第三张表进行操作
obj.r.remove() 
obj.r.clear() 清楚
obj.r.set() 更新

obj.r.all()  所有 相关的主机对象 queryset


app_name = request.POST.get('app_name')
host_list = request.POST.getlist('host_list')
obj = models.Application.objects.create(name=app_name)
obj.r.add(*host_list)

jquery中ajax中发送的列表的时候，要添加
traditional:true,


foreign 是一对多的关系
ManyToManyFiled  多对多的关系  双方互为对方的外键
用户和文章   一个用户对应多篇文章

怎样知道是哪个用户进行发送的数据
带cookie发送数据

```

