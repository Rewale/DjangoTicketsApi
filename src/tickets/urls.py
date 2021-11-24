from django.urls import path
from . import views

urlpatterns = [
    path("tickets/", views.TicketsInFlightListView.as_view()),
    path("flights/", views.FlightListView.as_view()),
    path("tickets/buy/<str:flight_num>/<int:seq>/", views.buy_ticket),
    path("tickets/myTickets/", views.UsersTickets.as_view()),
]