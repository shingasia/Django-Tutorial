"""
URL configuration for config project.

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
from django.urls import path
# from config.views import main, test1, test2, test3, test4
from config.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", main), # 공백(아무것도 입력하지 않은 경로)과 main 함수 연결
    path("testURL1/test1", test1),
    path("testURL1/test2", test2),
    path("testURL1/test3", test3),
    path("testURL1/test4", test4),
    path("testURL1/test5", test5),
    path("testURL1/test6", menu_list),
    path("testURL1/test7", menu_list2),
    path("books/", book_list),
    path("search/", book_search),
]
