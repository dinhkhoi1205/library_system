
from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin manage users, books, borrow records
    path('admin/', admin.site.urls),
    # Register new user
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    # Login endpoint - Use JWT token
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
     # Get a new access token using a refresh token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    # Login/Logout interface for django Rest framework
    path("api-auth", include("rest_framework.urls")),
    # Include core app api URL's
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)