from django.db import models

# Create your models here.

class UserInfo(models.Model):
    user_type = (
        (1,'普通用户'),
        (2,'VIP'),
        (3,'超级VIP'),
    )
    user_type = models.IntegerField(choices=user_type)
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)

class UserToken(models.Model):
    user = models.OneToOneField("UserInfo",on_delete=True)
    token = models.CharField(max_length=64)