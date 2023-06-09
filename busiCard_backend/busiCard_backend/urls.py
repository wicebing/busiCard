"""
URL configuration for busiCard_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from app1 import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/whoami/', views.get_current_user, name='get_current_user'),
    path('api/upload/logo/', views.UploadLogoView.as_view(), name='upload_logo'),
    path('api/upload/personalLinkImage/', views.UploadPersonalLinkImageView.as_view(), name='upload_personalLinkImage'),
    path('api/upload/deletePersonalLinkImage/', views.DeletePersonalLinkImageView.as_view(), name='delete_personalLinkImage'),
    path('api/regist/', views.UserGenericView.as_view(), name='regist'),
    path('api/regist/<pk>/', views.UserDetailGenericView.as_view()),
    path('api/businessCard/', views.BusinessCardGenericView.as_view(), name='businessCard'),
    path('api/businessCard/<pk>/', views.BusinessCardDetailGenericView.as_view()),
    path('api/personalLink/', views.PersonalLinkGenericView.as_view(), name='personalLink'),
    path('api/personalLink/<pk>/', views.PersonalLinkDetailGenericView.as_view()),
    path('api/linkIPClick/', views.LinkIPClickGenericView.as_view(), name='linkIPClick'),
    path('api/linkIPClick/<pk>/', views.LinkIPClickDetailGenericView.as_view()),
    path('api/linkClick/', views.LinkClickView.as_view(), name='link_click'),


    path('token/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
