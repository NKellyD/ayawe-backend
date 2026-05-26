from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import UserRegisterView,UserLoginView,UserListView,UserEmailView

router = DefaultRouter()
router.register('users-emails',UserEmailView,basename='users')

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/list/', UserListView.as_view(), name='user_list'),
    path("",include(router.urls)),

]