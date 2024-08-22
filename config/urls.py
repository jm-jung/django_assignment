"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.http import HttpResponse
from django.shortcuts import render
user_db = {
    1: {
        '이름': '머용',
        '나이': 27,
        '생년월일': '1998-08-29',
        '취미': '배드민턴',
        '거주지': '서울특별시 강서구',
        '개발경력': '2년 2개월'
    },
    2: {
        '이름': '수현',
        '나이': 30,
        '생일': '1995-02-22',
        '취미': '시체놀이',
        '거주지': '서울특별시 은평구',
        '개발경력': '2년 4개월'
    },
    3: {
        '이름': '유준',
        '나이': 29,
        '생일': '1996-03-11',
        '취미': '로스트아크',
        '거주지': '서울특별시 강서구',
        '개발경력': '3년 2개월'
    },
    4: {
        '이름': '승현',
        '나이': 28,
        '생일': '1997-01-16',
        '취미': '여행',
        '거주지': '서울특별시 강남구',
        '개발경력': '3년 5개월'
    },
    5: {
        '이름': '성훈',
        '나이': 33,
        '생일': '1992-09-21',
        '취미': '운동',
        '거주지': '경기도 고양시',
        '개발경력': '7년 4개월'
    }
}

def user_list(request):
    return render(request,'users.html',{'user_db':user_db})
def user_detail(request,index):
    if index in user_db:
        user = user_db[index]
        context = {'user':user,'user_id':index}
        return render(request,'user_detail.html',context)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', user_list),
    path('users/<int:index>/', user_detail),
]
