from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UserProfileForm, UserUpdateForm
from .models import UserProfile


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('routes:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile automatically
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(
                request, f'Welcome to Sayil, {user.username}! 🏔️'
            )
            return redirect('routes:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """User profile view with favorites."""
    # Ensure profile exists
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    favorites = user_profile.favorite_routes.all()
    user_reviews = request.user.reviews.select_related('route')

    context = {
        'user_profile': user_profile,
        'favorites': favorites,
        'user_reviews': user_reviews,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """Edit user profile."""
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
