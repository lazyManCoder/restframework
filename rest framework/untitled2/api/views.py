from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView,View
from rest_framework.request import  Request
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning #默认的参数  versioning_class = QueryParameterVersioning
from rest_framework.parsers import JSONParser,FormParser
from rest_framework import serializers
from api import models
# Create your views here.

class ParamVersion(object):
    def determine_version(self,request,*args,**kwargs):
        version = request.query_params.get('version')
        return version



class UsersView(APIView):
    versioning_class = URLPathVersioning         #ParamVersion
    def ge(self,request,*args,**kwargs):
        print(request.data)
        return HttpResponse('hello')
    def head(self,request,*args,**kwargs):
        return HttpResponse('hi')

import json
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['id','username']
        depth = 0

class UserInfo(APIView):
    def get(self,request,*args,**kwargs):
        user = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=user,many=True,context={'request':request})
        ser.data
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)

class XValidator(object):
    def __init__(self,base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '标题以 %s 为开头'%self.base
            raise serializers.ValidationError(message)

class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required':"标题不为空"},validators=[XValidator('小'),])

class Order(APIView):
    def post(self,request,*args,**kwargs):

        ser = UserGroupSerializer(data=request.data)   #进行一次判断
        print(hasattr(UserGroupSerializer, '_validated_data'))
        print(ser.initial_data)
        # print(ser.run_validation(ser.initial_data))

        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)
        return HttpResponse('提交数据')

from api.utils.serializsers.Pager import PagerSerialiser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
# class MyPagination(PageNumberPagination):
#     page_size = 2
#
#     page_size_query_param = 'size'  #'size'传递一个size参数
#     max_page_size = 5


# class MyPagination(LimitOffsetPagination):
#     default_limit = 2
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'
#     max_limit = 5     #分页类
class MyPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'
    page_size_query_param = None
    max_page_size = None

class PageView(APIView):
    def get(self,request,*args,**kwargs):
        roles = models.Role.objects.all()

        # ret = json.dumps(ser.data,ensure_ascii=False)
        # return HttpResponse(ret)
        pg = MyPagination()
        page_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        ser = PagerSerialiser(instance=page_roles,many=True)
        # return Response(ser.data)
        return pg.get_paginated_response(ser.data)


# from rest_framework.generics import GenericAPIView
# class V1View(GenericAPIView):
#     queryset = models.Role.objects.all()
#     serializer_class = PagerSerialiser
#     pagination_class = PageNumberPagination
#     def get(self,request,*args,**kwargs):
#         roles = self.get_queryset()
#         #进行分页
#         page_roles = self.paginate_queryset(roles)
#
#         #序列化
#         ser = self.get_serializer(instance=page_roles,many=True)
#         return Response(ser.data)


# from rest_framework.viewsets import GenericViewSet
# class V1View(GenericViewSet):
#     def get(self,request,*args,**kwargs):
#         return Response('...')

from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin
class V1View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerialiser
    pagination_class = PageNumberPagination

from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer,AdminRenderer,HTMLFormRenderer
class TestView(APIView):
    renderer_classes = [AdminRenderer,BrowsableAPIRenderer]
    def get(self,request,*args,**kwargs):
        roles = models.Role.objects.all()

        # ret = json.dumps(ser.data,ensure_ascii=False)
        # return HttpResponse(ret)
        pg = MyPagination()
        page_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        ser = PagerSerialiser(instance=page_roles,many=True)
        return Response(ser.data)
        #return pg.get_paginated_response(ser.data)


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