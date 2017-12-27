from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from comics.views.series import SeriesList, SearchSeriesList, SeriesDetail


app_name = 'series'
urlpatterns = [
    path('series/', SeriesList.as_view(), name='list'),
    path('series/<slug:slug>/', SeriesDetail.as_view(), name='detail'),
    re_path(r'^series/search/?$', SearchSeriesList.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
