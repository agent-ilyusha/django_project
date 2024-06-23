"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework import routers
from app.viewset_model import *
from app.views import (
    register,
    profile,
    PasswordChangeView,
    login_view,
    logout_view,
    settings_view,
    create_car,
    view_cars,
    view_car,
    settings_vehicle,
    buy_car,
    replenishment,
    delete_car
)

router = routers.DefaultRouter()
router.register(r'cars', CarViewSet)  # view set car
router.register(r'owners', OwnerViewSet)  # view set owner
router.register(r'addresses', AddressViewSet)  # view set address
router.register(r'services', ServiceRecordViewSet)  # view set service

# add urls
urlpatterns = [
    path('', profile, name='profile'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', register, name='register'),
    path('profile/', profile, name="profile"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/settings/', settings_view, name='settings'),
    path('car/create/', create_car, name='create_car'),
    path('car/views/', view_cars, name='view_cars'),
    path('car/view-car/', view_car, name='view_car'),
    path('car/settings/', settings_vehicle, name='settings_vehicle'),
    path('car/buy/', buy_car, name='buy_car'),
    path('profile/replenishment/', replenishment, name='replenishment'),
    path('car/delete/', delete_car, name='delete_car'),
    # path('cars/', CarViewSet.as_view(), name='cars'),
    # path('owners/', OwnerViewSet.as_view(), name='owners'),
    # path('addresses/', AddressViewSet.as_view(), name='addresses'),
    # path('serviceRecords/', ServiceRecordViewSet.as_view(), name='serviceRecords'),
]
