from django.urls import path
from ebook import views


urlpatterns = [
    path("create/", views.create_ebook, name="create_ebook"),
    path("<slug>/", views.detail_ebook, name="detail"),
    path("<slug>/edit/", views.edit_ebook, name="edit"),
    path("<slug>/like/", views.like, name="like"),
]
