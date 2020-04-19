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
import os
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from base_app import views as baseAppViews
from django.conf import settings
from base_app.models import UserRecord





urlpatterns = [

    path('admin/', admin.site.urls),
    path('home/',baseAppViews.home,name='register'),
    path('verify/',baseAppViews.verify,name='validate_pin'),
    path('view/',baseAppViews.view,name='view'),
    path('logout/',baseAppViews.logout_user,name="logout"),
    path('errors/',baseAppViews.check_errors,name='check_errors'),
    path('user_info/',baseAppViews.check_user,name="user_check"),
    path('import/',baseAppViews.import_users,name='import')
]

if(settings.OAUTH_ENABLED):

    from django.contrib.sites.models import Site
    from allauth.socialaccount.models import SocialAccount, SocialApp

    social_account = SocialApp.objects.get_or_create(provider="google",name="Google API",client_id =str(os.getenv("GOOGLE_CLIENT_ID")),secret=str(os.getenv("GOOGLE_CLIENT_SECRET")))
    if(social_account[1] !=False):
        social_account[0].sites.add(Site.objects.first())
    print(social_account[0].provider)
    urlpatterns += [
        path('', TemplateView.as_view(template_name='base_app/main.html')),
        path('accounts/', include('allauth.urls'))
        ]

else:
    urlpatterns += [path('',TemplateView.as_view(template_name='base_app/user_creation.html')),
                    path('login/',baseAppViews.login_user,name='login'),
                    path('register/',baseAppViews.register_user,name='register_user')]
    print("success")