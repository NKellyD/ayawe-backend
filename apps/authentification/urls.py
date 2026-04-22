from django.urls import path
from .views import UserRegisterView,UserLoginView,UserListView
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/list/', UserListView.as_view(), name='user_list'),

]