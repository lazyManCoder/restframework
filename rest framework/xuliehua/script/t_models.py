# author navigator
#django脚本化启动
import os,django
#想要起Django项目首先要加载配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xuliehua.settings') #项目先加载到内存中
django.setup() #socket

from api import models
# author = models.Author.objects.first()
# print(author.name)
# print(author.detail.mobile)
#
# detail = models.AuthorDetail.objects.first()
# print(detail.mobile)
# print(detail.author.name)


#1）作者删除，详情级联 - on_delete = models.CASCADE
#2) 作者删除，详情置空 - null = True on_delete = models.SET_NULL    详情外键置空
#3) 作者删除，详情重置 - default = 0 ,on_delete = models.SET_DEFAULT
#4) 作者删除，详情不动 - on_delete = models.DO_NOTHING
from api.utils.seralizer import serializser
ret = models.Book.objects.all()
res = serializser.BookModelSerializser(instance=ret)
print(res.data)
