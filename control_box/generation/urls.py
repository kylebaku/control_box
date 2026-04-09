from django.urls import path

from . import views


app_name = 'generation'

urlpatterns = [ 
    path('', views.generation, name='generation'),
    path('hand/', views.hand_creation, name='hand_creation'),
    path('automatic/', views.automatic_creation, name='automatic_creation'),
]