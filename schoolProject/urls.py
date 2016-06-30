"""schoolProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from e_homework.login_views import *

urlpatterns_auth = [
    url(r'^sign-in/do-sign-in/', do_sign_in, name='do-sign-in'),
    url(r'^sign-in/', sign_in),
    url(r'^sign-up/do-sign-up/', do_sign_up),
    url(r'^sign-up/', sign_up),
    url(r'^logout/', do_logout),
    url(r'get-school-list/', get_school_list),
    url(r'get-class-list/', get_class_list),
    url(r'validate-username/', validate_username, name='validate-username'),
    url(r'validate-password/', validate_password, name='validate-password'),
    url(r'validate-user/', validate_user, name='validate-user'),
    url(r'validate-password-for-user/', validate_password_for_user, name='validate-password-for-user')
]
urlpatterns = urlpatterns_auth + [
    url(r'^admin/', admin.site.urls),
    url(r'^$', lambda _: redirect("/sign-in/"), name='sign-in')
]
