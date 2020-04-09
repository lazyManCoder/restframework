from django.shortcuts import render
from rest_framework.views import View,APIView,status
from api import models
from api.exception.exception import exception_handler
from rest_framework.response import Response
# Create your views here.


from api.utils.seralizer import serializser
from django.conf import settings
class UseView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            # try:
                #用户对象不能直接返回给前台
                #序列话一下用户对户对象

            user_obj = models.User.objects.get(pk=pk)
            user_ser = serializser.UserSerializser(user_obj)
            return Response({
                'status':0,
                'msg':0,
                'results':user_ser.data
            })
            # except:
            #     return Response({
            #         'detail':'输错了吧哥'
            #     },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # return Response({
                #     'status':0,
                #     'msg':'用户不存在',
                # })
        else:
            user_obj_list = models.User.objects.all()
            user_ser_list = serializser.UserSerializser(instance=user_obj_list,many=True) #应该在内部定义循环
            print(user_ser_list)

            return Response({
                    'status':0,
                    'msg':0,
                    'results':user_ser_list.data
                })

    def post(self,request,*args,**kwargs):
        request_data = request.data
        #数据是否合法（增加对象是一个字典）
        print(request_data,type(request_data))
        if not isinstance(request_data,dict) or request_data == {}:
            return Response({
                'status':1,
                'msg':'数据有误'
            })

        #数据类型合法，但数据内容不一定合法，需要校验
        use_ser = serializser.UserDeserializer(data = request_data)
        if use_ser.is_valid():
            #校验通过,完成新增
            use_obj = use_ser.save()
            return Response({
            'status':0,
            'msg':'OK',
            'results':serializser.UserSerializser(use_obj).data
        })
        else:
            return Response({
                'status':1,
                'msg':use_ser.errors
            })

class Book(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Book.objects.get(pk=pk,is_delete=False)
            book_data = serializser.BookModelSerializser(book_obj)

        else:
            book_query = models.Book.objects.filter(is_delete=False).all()
            book_data = serializser.BookModelSerializser(book_query,many=True)
        return Response({
            'status':1,
            'result':book_data.data,

        })