from django.urls import path
from . import views

urlpatterns = [
    path("tickets/<str:flight_num>/<int:seq>", views.TicketsDetailView.as_view()),
    path("flights/<str:flight_num>", views.FlightDetailView.as_view()),
    path("flights/", views.FlightListView.as_view()),
    path("tickets/buy/", views.BuyTicket.as_view()),
    path("tickets/myTickets/", views.UsersTickets.as_view()),
]