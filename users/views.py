from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from movies.models import Movie, Booking
from django.utils import timezone

# Homepage view
def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})

# User registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# User login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# User profile with booking info and update option

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'theater', 'seat')
    now = timezone.now()

    upcoming = bookings.filter(theater__time__gte=now).order_by('theater__time')
    past = bookings.filter(theater__time__lt=now).order_by('-theater__time')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'upcoming': upcoming,
        'past': past
    })


# Password reset view
@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/reset_password.html', {'form': form})

# Static pages
def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    return render(request, 'pages/contact.html')
