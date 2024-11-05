from django.urls import path

from contract import views


urlpatterns = [
    path('debts/', views.DebtsView.as_view()), 
    path('my-borrowed-debts/', views.MyBorrowedDebtsView.as_view()),
    path('my-lent-debts/', views.GetAllDebtsView.as_view()),
    path('inactive-debts/', views.InactiveDebtsView.as_view()),
    path('change-debts-status/', views.ChangeDebtStatusView.as_view()),
    path('get-all-debts/', views.GetAllDebtsView.as_view()),
    path('get-debt/<int:pk>/', views.DetailedDebtView.as_view()),
]