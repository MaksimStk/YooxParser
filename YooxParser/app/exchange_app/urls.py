from django.urls import path
from .views import exchange
from . import views


urlpatterns = [
    path('', exchange, name='home'),
    path('documentation', views.documentation),
]