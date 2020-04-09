
# author navigator
#序列化组件为每一个modal类提供一套序列化工具类
#序列化组件的工作方式与django form组件十分相似
from rest_framework import serializers,exceptions
from django.conf import settings
from api import models

class UserSerializser(serializers.Serializer):
      name = serializers.CharField()
      pwd = serializers.CharField()
      phone = serializers.CharField()
      #序列化提供给前台的字段个数由后台决定，可以少提供
      #但是提供的数据对应的字段，名字一定要与数据库字段相同
      # sex = serializers.IntegerField()
      # icon = serializers.ImageField()

      #自定义序列化属性
      #属性名随意，值由固定的命名规范方法提供，get_属性名(self,参与序列化的model对象)
      gender = serializers.SerializerMethodField()
      def get_gender(self,obj):
          print(self,obj)
          return obj.get_sex_display()

      icon = serializers.SerializerMethodField()
      def get_icon(self,obj):
          print(settings.MEDIA_URL)
          return '%s%s%s'%('http://127.0.0.1:8000',settings.MEDIA_URL,str(obj.icon))


class UserDeserializer(serializers.Serializer):
    #哪些字段必须反序列化
    #字段都有哪些安全校验
    #哪些字段需要额外的提供校验
    #哪些字段间存在联合校验
    #反序列化字段都是用来入库，才出现自定义属性,会出现可以设置
    name = serializers.CharField(
        max_length=10,
        min_length=4,
        error_messages={
            'max_length':'太长',
            'min_length':'太短不好'
        }

    )
    pwd = serializers.CharField()
    phone = serializers.CharField(required=False)
    sex = serializers.IntegerField(required=False)

    #自定义有校验规则的反序列化字段
    re_pwd = serializers.CharField()


    #局部钩子validate_要校验的字段名，当前要校验的字段值
    #校验规则，校验通过返回原值，校验失败，抛出异常
    def validate_name(self,value):
        if 'p' in value.lower()[0]: #名字中不能出现特定的词汇
            raise exceptions.ValidationError("名字非法")
        return value

    #全局钩子,第一个是序列化对象，attrs系统与局部钩子校验通过的数据
    def validate(self, attrs):
        print('attrs',attrs)
        pwd = attrs.get('pwd')
        re_pwd = attrs.pop('re_pwd') #从校验规则中拿出来
        if not pwd or pwd != re_pwd:
            raise exceptions.ValidationError('前后密码不一致')
        return attrs

    #要完成新增，需要自己重写create方法
    def create(self, validated_data):

        return models.User.objects.create(**validated_data)

    #name pwd re_pwd 为必填字段
    #phone sex为选填字段

from rest_framework.serializers import ModelSerializer
class BookModelSerializser(serializers.ModelSerializer):
    class Meta:
        #序列化关联的model类
        model = models.Book
        #参与序列化的字段
        #fields = "__all__" #所有字段
        fields = ('name','price','fn','author_list')
        #exclude = ('name',) 刨除字段
        #depth = 0 自动深度
