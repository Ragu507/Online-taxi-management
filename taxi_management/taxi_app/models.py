from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    is_passenger = models.BooleanField(default=False)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='taxi_app_user_set',  # Updated related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='taxi_app_user_set',  # Updated related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)
    vehicle_image = models.ImageField(upload_to='vehicles/')
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    total_rides = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_type}"

class PassengerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('card', 'Card')], default='cash')

    def __str__(self):
        return self.user.username

class Ride(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True)
    passenger = models.ForeignKey(PassengerProfile, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Ride by {self.passenger.user.username} with {self.driver.user.username if self.driver else 'No driver'}"

class Payment(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('card', 'Card')])
    payment_time = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment for {self.ride}"

class Rating(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    driver_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    passenger_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating for Ride {self.ride.id}"

class RideRequest(models.Model):
    passenger = models.ForeignKey(PassengerProfile, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    request_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"Ride Request by {self.passenger.user.username}"
