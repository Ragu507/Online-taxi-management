from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DashboardView,
    PassengerProfileCreateView,
    DriverProfileCreateView,
    DriverProfileDetailView,
    PassengerProfileDetailView,
    PassengerProfileUpdateView,
    DriverProfileUpdateView,
    RideRequestCreateView,
    RideRequestUpdateView,
    RideRequestDeleteView,
    RideRequestAcceptView,
    RideRequestListView,
    RideCreateView,
    RideUpdateView,
    RideDeleteView,
    RideListView,
    CustomLoginView,
    PassengerProfileListView,
    DriverProfileListView
)

urlpatterns = [
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Passenger Profile URLs
    path('profiles/passenger/', PassengerProfileListView.as_view(), name='passenger-profile-list'),
    path('profile/passenger/create/', PassengerProfileCreateView.as_view(), name='passenger-profile-create'),
    path('profile/passenger/<int:pk>/', PassengerProfileDetailView.as_view(), name='passenger-profile-detail'),
    path('profile/passenger/<int:pk>/edit/', PassengerProfileUpdateView.as_view(), name='passenger-profile-update'),
    
    # Driver Profile URLs
    path('profile/driver/create/', DriverProfileCreateView.as_view(), name='driver-profile-create'),
    path('drivers/', DriverProfileListView.as_view(), name='driver-profile-list'),
    path('profile/driver/<int:pk>/', DriverProfileDetailView.as_view(), name='driver-profile-detail'),
    path('profile/driver/<int:pk>/edit/', DriverProfileUpdateView.as_view(), name='driver-profile-update'),

    # Ride Request URLs
    path('ride-request/create/', RideRequestCreateView.as_view(), name='ride-request-create'),
    path('ride-requests/', RideRequestListView.as_view(), name='ride-request-list'),
    path('ride-request/<int:pk>/edit/', RideRequestUpdateView.as_view(), name='ride-request-update'),
    path('ride-request/<int:pk>/delete/', RideRequestDeleteView.as_view(), name='ride-request-delete'),
    path('ride-request/<int:pk>/accept/', RideRequestAcceptView.as_view(), name='ride-request-accept'),

    # Ride URLs
    path('ride/create/', RideCreateView.as_view(), name='ride-create'),
    path('ride/<int:pk>/edit/', RideUpdateView.as_view(), name='ride-update'),
    path('ride/<int:pk>/delete/', RideDeleteView.as_view(), name='ride-delete'),
    path('ride/list/', RideListView.as_view(), name='ride-list'),
]
