from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView,CreateView,DeleteView,TemplateView,ListView
from .models import *
from .forms import PassengerProfileForm,DriverProfileForm,UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('dashboard') 

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_rides'] = Ride.objects.count()
        context['active_rides'] = Ride.objects.filter(status='accepted').count()
        context['upcoming_requests'] = RideRequest.objects.filter(status='pending').count()
        context['total_passengers'] = PassengerProfile.objects.count()
        context['total_drivers'] = DriverProfile.objects.count()
        return context

class PassengerProfileCreateView(CreateView):
    model = PassengerProfile
    form_class = PassengerProfileForm
    template_name = 'profiles/passenger_profile_form.html'
    success_url = reverse_lazy('passenger-profile-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserCreationForm(self.request.POST)
        else:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Get the user form
        user_form = self.get_context_data()['user_form']
        
        # Check if user form is valid
        if user_form.is_valid():
            # Save the user form to create the User instance
            user = user_form.save(commit=False)
            user.is_passenger = True  # Set is_passenger to True
            user.save()  # Save the user instance
            
            # Assign the user to the passenger profile
            form.instance.user = user
            
            # Log the user in after saving
            login(self.request, user)
            
            # Save the PassengerProfile and redirect to success URL
            return super().form_valid(form)
        else:
            # If the user form is invalid, return form invalid
            return self.form_invalid(form)

        
class PassengerProfileListView(LoginRequiredMixin, ListView):
    model = PassengerProfile
    template_name = 'profiles/passenger_profile_list.html'
    context_object_name = 'passenger_profiles'
    paginate_by = 10  # Adjust the number of items per page as needed

    def get_queryset(self):
        return PassengerProfile.objects.all()

class DriverProfileCreateView(CreateView):
    model = DriverProfile
    form_class = DriverProfileForm
    template_name = 'profiles/driver_profile_form.html'
    success_url = reverse_lazy('driver-profile-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserCreationForm(self.request.POST)
        else:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        if user_form.is_valid():
            # Save the user, but don't commit yet
            user = user_form.save(commit=False)
            user.is_driver = True  # Set is_driver to True, as it's a Driver creation
            user.save()
            
            # Attach the created user to the DriverProfile instance
            form.instance.user = user
            login(self.request, user)
            return super().form_valid(form)
        else:
            # If user form is invalid, re-render the page with both forms and errors
            return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self):
        """Pass POST data to both forms."""
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES
            })
        return kwargs
    

class DriverProfileListView(ListView):
    model = DriverProfile
    template_name = 'profiles/driver_profile_list.html'
    context_object_name = 'driver_profiles'
    paginate_by = 10  # Number of profiles per page

    def get_queryset(self):
        return DriverProfile.objects.all()


class DriverProfileDetailView(LoginRequiredMixin, DetailView):
    model = DriverProfile
    template_name = 'profiles/driver_profile.html'
    context_object_name = 'driver'

class PassengerProfileDetailView(LoginRequiredMixin, DetailView):
    model = PassengerProfile
    template_name = 'profiles/passenger_profile.html'
    context_object_name = 'passenger'

class PassengerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = PassengerProfile
    fields = ['preferred_payment_method']
    template_name = 'profiles/passenger_profile_edit.html'
    success_url = '/profile/passenger/'

class DriverProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = DriverProfile
    fields = ['license_number', 'vehicle_type', 'vehicle_model', 'vehicle_number', 'vehicle_image']
    template_name = 'profiles/driver_profile_edit.html'
    success_url = reverse_lazy('driver-profile-list')


class RideRequestCreateView(LoginRequiredMixin, CreateView):
    model = RideRequest
    fields = ['passenger', 'pickup_location', 'dropoff_location']
    template_name = 'riderequests/ride_request_form.html'
    success_url = reverse_lazy('ride-request-list')

class RideRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = RideRequest
    fields = ['pickup_location', 'dropoff_location', 'status']
    template_name = 'riderequests/ride_request_form.html'
    success_url = reverse_lazy('ride-request-list')

class RideRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = RideRequest
    template_name = 'riderequests/ride_request_confirm_delete.html'
    success_url = reverse_lazy('ride-request-list')

class RideRequestListView(LoginRequiredMixin, ListView):
    model = RideRequest
    template_name = 'riderequests/ride_request_list.html'
    context_object_name = 'ride_requests'
    paginate_by = 10  # Number of requests per page

    def get_queryset(self):
        user = self.request.user
        if user.is_driver:
            print("User is driver")
            return RideRequest.objects.filter(status='pending')
        elif user.is_passenger:
            print("User is passenger")
            return RideRequest.objects.filter(passenger=user.passengerprofile)
        else:
            print("User is neither driver nor passenger")
            return RideRequest.objects.none()




class RideRequestAcceptView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ride_request_id = kwargs.get('pk')
        ride_request = get_object_or_404(RideRequest, id=ride_request_id)
        
        if not request.user.is_driver:
            return redirect('dashboard')  # or an appropriate error page

        driver = DriverProfile.objects.get(user=request.user)
        
        ride = Ride.objects.create(
            driver=driver,
            passenger=ride_request.passenger,
            pickup_location=ride_request.pickup_location,
            dropoff_location=ride_request.dropoff_location,
            pickup_time=ride_request.request_time, 
            status='accepted'
        )
        
        # Update the RideRequest status
        ride_request.status = 'accepted'
        ride_request.save()
        
        return redirect('dashboard')
    
class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['driver', 'passenger', 'pickup_location', 'dropoff_location', 'pickup_time', 'dropoff_time', 'status', 'fare']
    template_name = 'rides/ride_form.html'
    success_url = reverse_lazy('ride-list')

class RideUpdateView(LoginRequiredMixin, UpdateView):
    model = Ride
    fields = ['driver', 'passenger', 'pickup_location', 'dropoff_location', 'pickup_time', 'dropoff_time', 'status', 'fare']
    template_name = 'rides/ride_form.html'
    success_url = reverse_lazy('ride-list')

class RideDeleteView(LoginRequiredMixin, DeleteView):
    model = Ride
    template_name = 'rides/ride_confirm_delete.html'
    success_url = reverse_lazy('ride-list')

class RideListView(LoginRequiredMixin, ListView):
    model = Ride
    template_name = 'rides/ride_list.html'
    context_object_name = 'rides'
    paginate_by = 10  # Number of rides per page

    def get_queryset(self):
        # Optionally, you can filter rides based on user roles or other criteria
        return Ride.objects.all()
