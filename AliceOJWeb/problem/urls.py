from django.urls import path
from . import views


app_name = 'problem'

urlpatterns = [
    path('submit/', views.problem_submit, name='submit'),
    path('list/', views.problem_list, name='list'),
    path('<int:id>/', views.problem_detail, name='detail'),
]
