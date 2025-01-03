from django.urls import path 
from .views import homeback , home
urlpatterns = [    
    path('',homeback ,name='homeback'), # http://127.0.0.1:8000/
    path('home',home ,name='home'),
]
