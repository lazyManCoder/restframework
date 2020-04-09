# author navigator

from rest_framework import exceptions
from app import models
from rest_framework.authentication import BaseAuthentication

class MyAuthentication1(BaseAuthentication):
    def authenticate(self,request):
        pass

    def authenticate_header(self, request):

        pass


class MyAuthentication(BaseAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()

        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        #在内部会将这两个字段赋值给request
        return (token_obj.user,token_obj)

    def authenticate_header(self, request):

        pass
