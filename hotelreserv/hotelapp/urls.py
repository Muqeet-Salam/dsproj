from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name= 'home'),
    path('final',views.final, name = 'final'),
    path('availableroom',views.availableroom, name='availableroom'),
    path('',views.home, name = 'bookroom'),
    path('checkout', views.checkout, name = 'checkout'),
    path('checkedout', views.checkedout, name = 'checkedout')

     

]