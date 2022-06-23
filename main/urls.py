"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from table_book.views import TablesViewSet, ApplicationViewSet, BookingViewSet, AppWithBookViewSet, FreeTablesViewSet, \
    AppWithoutBookViewSet

router = SimpleRouter()
router.register(r'table', TablesViewSet)
router.register(r'application', ApplicationViewSet)
router.register(r'booking', BookingViewSet, basename='book')
router.register(r'app_with_book', AppWithBookViewSet, basename='app_with_book')
router.register(r'free_tables', FreeTablesViewSet, basename='free_tables')
router.register(r'app_without_book', AppWithoutBookViewSet, basename='app_without_book')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]

