from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import (BookViewSet, CreateUserView, BorrowBookView,
                    ReturnBookView, UserBorrowedBooksView)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="Library management API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    # Register new user for testing
    # path("register/", CreateUserView.as_view(), name="register"),
    # Allow user to borrow books
    path("borrow/", BorrowBookView.as_view(), name="borrow-book"),
    # View list current book borrowed
    path("borrowed/", UserBorrowedBooksView.as_view()),
    # Return a book
    path("return/", ReturnBookView.as_view(), name="return-book"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("", include(router.urls)),
]
