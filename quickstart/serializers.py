from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Items, Cart
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class LoginSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class ItemsSerializer(serializers.ModelSerializer):

    #comments = serializers.CharField(max_length=155, write_only=True)
    #list_price = serializers.ListField(source='user.username')

    class Meta:
        model = Items
        fields = ('id', 'name', 'price', 'description')

    """def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance"""

    """def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance"""


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('user', 'item',)


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', )