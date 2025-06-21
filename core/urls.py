from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('page404/', Page404View.as_view(), name='404page'),
    path('categories/<int:pk>/articles/', CategoryArticleView.as_view(), name='article'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-details'),
    path('contact-us/', ContactView.as_view(), name='contact-us')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)