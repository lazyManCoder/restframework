from django.shortcuts import render,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework import exceptions
from django.http import JsonResponse
# class MyAuthentication(object):
#     def authenticate(self,request):
#         token = request._request.GET.get('token')
#         if not token:
#             raise exceptions.AuthenticationFailed('user failed')
#         return ('alex',None)
#
#     def authenticate_header(self,val):
#         pass




ORDER_DICT = {
    1:{
        'name':'apple',
        'age':2,
        'content':'....'
    },
   2:{
        'name':'dog',
        'age':3,
        'content':'....'
    }
}
class order(APIView):
    """
    订单相关业务
    """

    def get(self,request,*args,**kwargs):
        # print(Request.parser_context)
        ret = {
            'code':200,
            'msg':None,
            'data':None,
        }
        try:
            # token = request._request.GET.get('token')
            # if not token:
            #     return HttpResponse('未登录')
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

from app import models
def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding="utf-8"))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """
    用于用户登录认证
    """
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        ret = {'code':1000,'msg':None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')

            obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            token = md5(user)
            #存在就更新，不在就创建
            models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '登陆异常'
        return JsonResponse(ret)

class UserInfoView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,request,*args,**kwargs):

        print(request.user)
        return HttpResponse("用户信息")