from django.urls import path
from spending.views import SignupView,GetmeView,ExpenseListCreateView
from spending.views import ExpenseRetirveUpdateView
from rest_framework.authtoken.views import ObtainAuthToken
from spending.views import ExpenseSummary,BudegetPlanView
urlpatterns=[

    
    path("register/",SignupView.as_view()),

    path("getme/",GetmeView.as_view()),

    path("expense/",ExpenseListCreateView.as_view()),

    path("expense/<int:pk>/",ExpenseRetirveUpdateView.as_view()),

    path("summary/",ExpenseSummary.as_view()),

    path("budget/",BudegetPlanView.as_view()),

    path("token/",ObtainAuthToken.as_view())



]