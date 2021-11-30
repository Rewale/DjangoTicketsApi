from django.urls import path
from .endpoint import views, auth_view

urlpatterns = [
    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('google/', auth_view.google_auth),
    path('mail_pass_auth/', auth_view.mail_auth),
    path('mail_pass_reg/', auth_view.mail_reg),
    path('mail_pass_accept/', auth_view.mail_accept),
    path('', auth_view.google_login),
]