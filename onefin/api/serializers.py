import uuid
from rest_framework import serializers
from .models import Collection, AppUser

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['uuid', 'user', 'title', 'description', 'movies']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['uuid', 'name', 'password']