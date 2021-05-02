from django.urls import path
from distance.views import GeocodingApiView, DistanceMatrixApiView


urlpatterns = [
    path('geocoding', GeocodingApiView.as_view(), name="geocoding-api"),
    path('distance', DistanceMatrixApiView.as_view(), name="distance-matrix-api"),
]