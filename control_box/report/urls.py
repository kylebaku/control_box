from django.urls import path

from . import views


app_name = 'report'

urlpatterns = [
    path('', views.report, name='report'),
    path('<pk>/', views.report_list, name='report_list'),
]
