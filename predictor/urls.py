from django.urls import path
from django.urls import include
from . import views


urlpatterns = [
    path('',views.index , name='index'),
   
    path('signup',views.signup , name='signup'),
    path('signin',views.signin , name='signin'),
    path('signout',views.signout , name='signout'),
    path('contact',views.contact , name='contact'),
    path('about',views.about , name='about'),
    
    
]
