"""my_website URL Configuration

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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('video/<int:idx>/', views.run_video_information),
    path('up/<int:idx>/', views.run_up_information),
    path('search/', views.run_search),
    path('search_result/', views.run_search_result),
    path('creator/', views.run_creator),
    path('home/', views.run_homepage),
    path('<path:sth>', views.run_homepage),
    path('', views.run_homepage)
]
