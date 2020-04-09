# author navigator
from api import models
from rest_framework import serializers

class PagerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"