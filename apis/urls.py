from django.urls import path, include
from apis.views import router

urlpatterns = [
    path('', include(router.urls)),
]
