from django.urls import path

from lectionary import views

urlpatterns = [
    path("", views.index, name="index"),
]
