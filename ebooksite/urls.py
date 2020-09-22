from django.contrib import admin
from django.urls import path, include
from ebook import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.ebook_posts, name='ebook_posts'),
    path('registration/', include('account_manager.urls')),
    path('ebooks/', include('ebook.urls')),
    path('admin/', admin.site.urls),


    # REST_FRAMEWORK
    path('api/ebooks/', include('ebook.api.urls')),
    path('api/registration/', include('account_manager.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
