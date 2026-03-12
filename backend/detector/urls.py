from django.urls import path  # type: ignore
from .views import DetectFakeNews, DetectFakeNewsFromImage

urlpatterns = [
    path('detect/', DetectFakeNews.as_view(), name='detect_fake_news'),
    path('detect-image/', DetectFakeNewsFromImage.as_view(), name='detect_fake_news_image'),
]
