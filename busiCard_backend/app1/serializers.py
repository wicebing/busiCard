from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import F, ExpressionWrapper, IntegerField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("帳號已存在")
        return value
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("信箱已存在")
        return value
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)   
    
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token']
    def get_token(self, obj):
        token = TokenObtainPairSerializer.get_token(obj)
        return str(token)

class BusinessCardSerializer(serializers.ModelSerializer):
    AUTH_name = serializers.StringRelatedField(source='user.username', read_only=True)
    
    class Meta:
        model = Table_businessCard
        fields = '__all__'
        extra_fields = ['AUTH_name']

    
class PersonalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table_personalLink
        fields = '__all__'
    def validate(self, data):
        if data['startDate'] > data['endDate']:
            raise serializers.ValidationError("開始日期不能大於結束日期")
        return data
    


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
