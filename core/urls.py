from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('interaction/', views.interaction, name='interaction'),
    path('task-tracker/', views.task_tracker, name='task_tracker'),
    path('chatbot/', views.chatbot_interaction, name='chatbot_interaction'),
]