from django.urls import path
from front.views import FrontView 


urlpatterns = [
    path('', FrontView.as_view(), name="front")
]