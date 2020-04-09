# author navigator
#序列化组件为每一个modal类提供一套序列化工具类
#序列化组件的工作方式与django form组件十分相似
from rest_framework import serializers
class UserSerializser(serializers.Serializer):
      name = serializers.CharField()
      phone = serializers.CharField()
      sex = serializers.IntegerField()
      icon = serializers.ImageField()
