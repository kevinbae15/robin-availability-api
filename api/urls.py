"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.contrib import admin

from api.views.views import *
from api.views.v1availability import availability as v1availability
from api.views.v2availability import availability as v2availability
from api.views.v3availability import availability as v3availability

urlpatterns = [
    path("v1/availability", v1availability.as_view(), name="v1availability"),
    path("v2/availability", v2availability.as_view(), name="v2availability"),
    path("v3/availability", v3availability.as_view(), name="v3availability"),
]
