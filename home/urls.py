from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),                # Home / Add Task — only if logged in
    path('tasks/', views.tasks, name='tasks'),         # View tasks
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
