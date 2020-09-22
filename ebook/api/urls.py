from django.urls import path
from ebook.api.views import api_detail_ebook
from .import views
from .views import ApiEbookList


urlpatterns = [
    path('<slug>/', views.api_detail_ebook, name='detail'),
    path('<slug>/update', views.api_update_ebook, name='update'),
    path('<slug>/delete', views.api_delete_ebook, name='delete'),
    path('create', views.api_create_ebook, name='create'),
    path('list', ApiEbookList.as_view(), name='list'),
]
