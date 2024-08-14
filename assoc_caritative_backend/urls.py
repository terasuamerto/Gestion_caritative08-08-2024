from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/',register, name='register'),
    path('api/login/', login, name='login'),
    path('user-info/', get_user_info, name='get_user_info'),
    path('api/creer_cagnotte/',creer_cagnotte, name='creer_cagnotte'),
    #path('cagnottes/', liste_cagnottes, name='liste_cagnottes'),
    path('api/faire_don', faire_don, name='faire_don'),
]

