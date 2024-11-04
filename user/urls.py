from django.urls import path

from user import views  


urlpatterns = [
    path('login/', views.LoginView.as_view()),  
    path('register/', views.RegisterView.as_view()),  
]