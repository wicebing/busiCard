from datetime import datetime, timedelta

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, get_list_or_404

from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .permissions import IsOwnerOrAdmin

# Create your views here.
class UserGenericView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filter_fields = ('is_staff')
    ordering_fields = ('NTUHid','name')
    search_fields = ('is_staff')
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return []
    
    def get_queryset(self):
        queryset = User.objects.all()
        is_staff = self.request.query_params.get('is_staff', None)
        if is_staff is not None:
            if is_staff.lower() == 'true':
                queryset = queryset.filter(is_staff=True)
            elif is_staff.lower() == 'false':
                queryset = queryset.filter(is_staff=False)
        return queryset

class UserDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    permission_classes = (IsOwnerOrAdmin,)
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsOwnerOrAdmin,]
        if self.request.method == 'GET':
            return [permissions.IsAdminUser(),]
        return []

 



@api_view(['GET'])
# @permission_classes([IsStaff])
@authentication_classes([JWTAuthentication,SessionAuthentication])
def get_current_user(request):
    user = request.user
    print(request.user.id,request.user.username,request.user.email)
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    }, status=status.HTTP_200_OK)