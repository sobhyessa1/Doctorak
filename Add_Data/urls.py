from django.urls import path
from .views import add_and_search_disease 

urlpatterns = [
    path('add/', add_and_search_disease, name='add_medical_record'),  # http://127.0.0.1:8000/add_data/add/
]
