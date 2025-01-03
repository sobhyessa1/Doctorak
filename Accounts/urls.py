from django.urls import path
from .views import signin, signup, account, logout, forget_reset_pass, search ,contact_view

urlpatterns = [
    path('', signup, name='signup'), # http://127.0.0.1:8000/accounts/
    path('signin', signin, name='signin'), # http://127.0.0.1:8000/accounts/signin
    path('logout', logout, name='logout'),  # http://127.0.0.1:8000/accounts/logout
    path('account', account, name='account'), # http://127.0.0.1:8000/accounts/account
    path('forget_reset_pass', forget_reset_pass, name='forget_reset_pass'), # http://127.0.0.1:8000/accounts/forget_reset_pass
    path('search', search, name='search'), # http://127.0.0.1:8000/accounts/search
    path('contact_us', contact_view, name='contact_us'),

]
