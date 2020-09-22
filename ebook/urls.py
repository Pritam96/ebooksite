from django.urls import path
from ebook import views


urlpatterns = [
    path('all/', views.ebook_posts, name='ebook_posts'),
    path('create/', views.create_ebook, name='create_ebook'),
    path('<slug>/', views.detail_ebook, name='detail_ebook'),
    path('<slug>/edit/', views.edit_ebook, name='edit'),
]
