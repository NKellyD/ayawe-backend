from django.urls import path,include
from rest_framework import routers

from .views import AccountView,CategoryTypeListView,CategoryView,TargetView,ContributionView

router = routers.DefaultRouter()
router.register('targets', TargetView, basename='target')
router.register('contributions', ContributionView, basename='contribution')
router.register('accounts', AccountView, basename='account')

urlpatterns = [
    path('categories-type/', CategoryTypeListView.as_view(), name='categories-type'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path("", include(router.urls)),
]

