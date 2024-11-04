from django.urls import path

from contract import views


urlpatterns = [
    path('', views.Contractview.as_view()), 
]