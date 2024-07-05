"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import UserView,UserDetailView,UserOrganizationView,UserOrganizationDetailView,UserByRoleView,UserByProfessorView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/user/', UserView.as_view()),
    path('api/user/role/<str:user_role>', UserByRoleView.as_view()),
    path('api/user/professor/', UserByProfessorView.as_view()),
    path('api/user/<int:pk>/', UserDetailView.as_view()),
    path('api/user/<int:user_pk>/organization/', UserOrganizationView.as_view()),
    path('api/user/<int:user_pk>/organization/<int:pk>/', UserOrganizationDetailView.as_view()),

    path('api/token/',TokenObtainPairView.as_view(), name="get_token"),
    path('api/token/refresh',TokenRefreshView.as_view(), name="refresh"),

    path('api-auth/', include("rest_framework.urls")),
    path('api/', include("api.urls")),
]
