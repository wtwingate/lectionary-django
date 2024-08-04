from django.urls import path

from lectionary import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("<int:pk>/", views.detail, name="detail"),
]
