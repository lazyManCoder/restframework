from django.db import models

# Create your models here.

class UserGroup(models.Model):
    title = models.CharField(max_length=32)

class Role(models.Model):
    title = models.CharField(max_length=32)

class UserInfo(models.Model):
    user_type = (
        (1,'普通用户'),
        (2,'VIP'),
        (3,'超级VIP'),
    )
    user_type = models.IntegerField(choices=user_type)
    group = models.ForeignKey("UserGroup",on_delete=True)
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)
    roles = models.ManyToManyField("Role")

class UserToken(models.Model):
    user = models.OneToOneField("UserInfo",on_delete=True)
    token = models.CharField(max_length=64)

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