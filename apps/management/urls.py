from django.urls import path
from .views import AccountView,CategoryTypeView,CategoryView

urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('categories-type/', CategoryTypeView.as_view(), name='categories-type'),
    path('categories/', CategoryView.as_view(), name='categories'),
]