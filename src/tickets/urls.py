from django.urls import path
from . import views

urlpatterns = [
    path('bought_tickets/', views.UsersTickets.as_view()),
]