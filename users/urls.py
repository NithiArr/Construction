from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('users/', views.manage_users_view, name='manage_users'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
]
