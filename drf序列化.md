# drf序列化

产生的原因

```python
用户从数据库中取出的数据不能直接返回给前台
我们就可以通过序列化将queryset类型中的数据进行转换
```



创建数据库

```pytho
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







我们要自定义我们的serializser方法

```python
# author navigator
#序列化组件为每一个modal类提供一套序列化工具类
#序列化组件的工作方式与django form组件十分相似
from rest_framework import serializers
from django.conf import settings
class UserSerializser(serializers.Serializer):
      name = serializers.CharField()
      pwd = serializers.CharField()
      phone = serializers.CharField()
      # sex = serializers.IntegerField()
      # icon = serializers.ImageField()  #我们可以任意隐藏我们的操作

      #自定义序列化属性
      #属性名随意，值由固定的命名规范方法提供，get_属性名(self,参与序列化的model对象)
      gender = serializers.SerializerMethodField()
      def get_gender(self,obj):
          print(self,obj)
          return obj.get_sex_display()

      icon = serializers.SerializerMethodField()
      def get_icon(self,obj):
          return '%s%s%s'%('http://127.0.0.1:8000',settings.MEDIA_URL,str(obj.icon))
```

在views.py

```python
from api.utils.serializsers import serializsers
class UseView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                #用户对象不能直接返回给前台
                #序列话一下用户对户对象

                user_obj = models.User.objects.get(pk=pk)
                user_ser = serializsers.UserSerializser(user_obj)
                return Response({
                    'status':0,
                    'msg':0,
                    'results':{

                    }
                })
            except:
                return Response({
                    'status':0,
                    'msg':'用户不存在',
                })
        else:
            user_obj_list = models.User.objects.all()
            return Response({
                    'status':0,
                    'msg':0,
                    'results':user_obj_list
                })
```

学会使用了

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

from django.conf import settings
将传递的媒体文件进行拼接传递到前端
icon = serializers.SerializerMethodField()
      def get_icon(self,obj):
          print(settings.MEDIA_URL)
          return '%s%s%s'%('http://127.0.0.1:8000',settings.MEDIA_URL,str(obj.icon))
```

学到了怎样配置admin

```python
from . import models
admin.site.register(models.User)
```

序列化的使用，可以用在查看信息，然后自定义属性的