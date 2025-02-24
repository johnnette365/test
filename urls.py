
from django.conf import settings
from django.urls import path
from Megazine import views
from django.conf.urls.static import static
from .views import magazine_list, magazine_detail




urlpatterns = [
    path("", views.home, name="home"),
    # path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    # path('', magazine_list, name='magazine_list'),
    path('magazine/<slug:slug>/', magazine_detail, name='magazine_detail'),
    # path('create/', magazine_create, name='magazine_create'),
    # path('magazine/<slug:slug>/comment/', add_comment, name='add_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)