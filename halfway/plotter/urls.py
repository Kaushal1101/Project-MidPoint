from django.urls import path
from . import views

app_name = 'plotter'
urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout_view"),
    path("load_places", views.load_places, name="load_places"),
    path("add_place", views.add_place, name="add_place"),
    path("delete_place", views.delete_place, name="delete_place")
]