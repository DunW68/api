"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from quickstart import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
#router.register(r'login', views.UserLogin, basename='Login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    #path('auth/', include('rest_framework.urls')),
    path('api/login/', views.UserLogin.as_view()),
    path('items/', views.ItemsView.as_view()),
    path('items/<int:pk>/', views.DetailView.as_view()),
    path('cart/', views.CartView.as_view()),
    url(r'^auth/', include('djoser.urls')),
    #url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('tokencheck/', views.TokenCheck.as_view()),
]


urlpatterns += staticfiles_urlpatterns()