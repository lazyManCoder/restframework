# author navigator
from rest_framework import exceptions
from app import models
from rest_framework.permissions import BasePermission

class SvipView(BasePermission):
    message = "必须是SVIP才可以访问"
    def has_permission(self,request,view):
        return False