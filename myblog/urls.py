from django.contrib import admin
from django.urls import path, include
from myblog import views

urlpatterns = [
    #API to post a comment
    path('postcomment', views.postcomment, name='postcomment'),

    path('', views.bloghome, name='bloghome'),
    path('<str:slugg>', views.blogpost, name='blogpost'),
]
