
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
     path('',views.user_login,name='user_login'),
     path('compose/',views.compose,name='compose'),
     path('inbox/',views.inbox,name='inbox'),
     path('sent/',views.sent,name='sent'),
     path('inbox/<int:id>/',views.view_mail_inbox,name='view_mail_inbox'),
     path('sent/<int:id>/',views.view_mail_sent,name='view_mail_sent'),
     path('logout/',views.user_logout,name='user_logout'),
     path('query/',views.query,name='query'),
]
