"""telegram_users_add URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.generic import TemplateView
from base_app import views as baseAppViews

urlpatterns = [
    path('', TemplateView.as_view(template_name='base_app/main.html')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('home/',baseAppViews.home,name='register'),
    path('verify/',baseAppViews.verify,name='validate_pin'),
    path('view/',baseAppViews.view,name='view'),
    path('logout/',baseAppViews.logout_user,name="logout"),
    path('errors/',baseAppViews.check_errors,name='check_errors')
]
