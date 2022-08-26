from django.urls import path
from . import views


app_name = 'user'

# 此处修改路由之后，base.html 对应的地方也需要进行修改，根据报错进行即可
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('center/', views.center, name="center"),
    path('rank/', views.rank, name='rank'),
]

