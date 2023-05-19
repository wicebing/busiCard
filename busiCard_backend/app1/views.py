from datetime import datetime, timedelta, date

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, get_list_or_404

from rest_framework import filters, views, parsers, status
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

class BusinessCardGenericView(generics.ListCreateAPIView):
    queryset = Table_businessCard.objects.all()
    serializer_class = BusinessCardSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)

    permission_classes = (IsOwnerOrAdmin,permissions.IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return []
    
    def get_queryset(self):
        queryset = Table_businessCard.objects.all()
        user = self.request.query_params.get('user', None)
        auth = self.request.query_params.get('auth', None)
        if user is not None:
            queryset = queryset.filter(user=user)
        if auth is not None:
            queryset = queryset.filter(user__username=auth)
        return queryset
    
class BusinessCardDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_businessCard.objects.all()
    serializer_class = BusinessCardSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    permission_classes = (IsOwnerOrAdmin,permissions.IsAuthenticatedOrReadOnly,)
    
class PersonalLinkGenericView(generics.ListCreateAPIView):
    queryset = Table_personalLink.objects.all()
    serializer_class = PersonalLinkSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)

    permission_classes = (IsOwnerOrAdmin,permissions.IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return []
    
    def get_queryset(self):
        queryset = Table_personalLink.objects.all()
        user = self.request.query_params.get('user', None)
        active = self.request.query_params.get('active', None)
        if user is not None:
            queryset = queryset.filter(user=user)
        
        if active is not None:
            # Filter where endDate is greater than today
            queryset = queryset.filter(endDate__gt=date.today())
            # Filter where startDate is less than today
            queryset = queryset.filter(startDate__lt=date.today())
        return queryset
    
class PersonalLinkDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table_personalLink.objects.all()
    serializer_class = PersonalLinkSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication,)
    permission_classes = (IsOwnerOrAdmin,permissions.IsAuthenticatedOrReadOnly,)





@authentication_classes([JWTAuthentication,SessionAuthentication])
class UploadLogoView(views.APIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')

        if not file:
            return Response({"file": ["No file uploaded!"]}, status=status.HTTP_400_BAD_REQUEST)

        # Here, `request.user` is the user who is uploading the file. Replace this with
        # the actual user who should be associated with the file.
        business_card = Table_businessCard.objects.get(user=request.user)

        business_card.logo = file
        business_card.save()

        return Response(status=status.HTTP_204_NO_CONTENT)



class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

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

