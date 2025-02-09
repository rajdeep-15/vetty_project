'''URL for the app'''

from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('crypto.urls')),
    path('api/token',TokenObtainPairView.as_view(),name='obtain_token_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='obtain_refresh_token')
]
