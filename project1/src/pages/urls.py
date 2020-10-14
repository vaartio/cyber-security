from django.urls import path

from .views import homePageView

urlpatterns = [
    path('', homePageView, name='home'),
    #path('add', homePageView, name='add'),
    #path('remove', homePageView, name='remove'),
]
