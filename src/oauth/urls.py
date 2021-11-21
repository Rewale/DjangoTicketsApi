from django.urls import path
from .endpoint import views, auth_view

urlpatterns = [
    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('google/', auth_view.google_auth),
    path('', auth_view.google_login),
]