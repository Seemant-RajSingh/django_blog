from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/', views.posts, name='posts'),  # List all posts
    path('post/<str:pk>/', views.post, name='post'),  # View individual post
    path('createpost/', views.createpost, name='createpost'),
    path('create/', views.create, name='create'),
    path('post/<int:pk>/editpost/', views.editpost, name='editpost'),
    path('post/<int:pk>/delete/', views.deletepost, name='deletepost'),

]
