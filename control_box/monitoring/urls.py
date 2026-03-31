from django.urls import path

from . import views


app_name = 'monitoring'

urlpatterns = [ 
    path('', views.monitoring, name='monitoring'),
    path('<pk>/', views.monitoring_detail, name='monitoring_detail'),
]