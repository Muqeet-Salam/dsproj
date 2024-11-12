from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('final', views.final, name='final'),
    path('availableroom', views.availableroom, name='availableroom'),
    path('checkout', views.checkout, name='checkout'),
    path('checkedout', views.checkedout, name='checkedout'),
    path('checkreservation', views.checkreservation, name='checkreservation'),
    path('contact/', views.contact, name='contact'),
]