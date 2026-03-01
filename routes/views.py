from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Route, Category, Review
from .forms import RouteForm, ReviewForm


def home(request):
    """Home page with hero and featured routes."""
    featured_routes = Route.objects.filter(
        is_published=True
    ).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating', '-created_at')[:6]
    categories = Category.objects.all()
    total_routes = Route.objects.filter(is_published=True).count()
    context = {
        'featured_routes': featured_routes,
        'categories': categories,
        'total_routes': total_routes,
    }
    return render(request, 'home.html', context)


def route_list(request):
    """List all published routes with filtering."""
    routes = Route.objects.filter(is_published=True).annotate(
        avg_rating=Avg('reviews__rating')
    )

    # Search
    query = request.GET.get('q', '')
    if query:
        routes = routes.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
        )

    # Filter by difficulty
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        routes = routes.filter(difficulty=difficulty)

    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        routes = routes.filter(categories__slug=category_slug)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = [
        'title', '-title', 'distance_km', '-distance_km',
        'created_at', '-created_at', 'avg_rating', '-avg_rating',
    ]
    if sort in valid_sorts:
        routes = routes.order_by(sort)

    categories = Category.objects.all()
    context = {
        'routes': routes,
        'categories': categories,
        'query': query,
        'difficulty': difficulty,
        'category_slug': category_slug,
        'sort': sort,
    }
    return render(request, 'routes/route_list.html', context)


def route_detail(request, slug):
    """Route detail page with reviews."""
    route = get_object_or_404(Route, slug=slug, is_published=True)
    reviews = route.reviews.select_related('user')
    user_review = None
    review_form = None
    is_favorited = False

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()
        if hasattr(request.user, 'profile'):
            is_favorited = request.user.profile.favorite_routes.filter(
                pk=route.pk
            ).exists()

    context = {
        'route': route,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
        'avg_rating': route.average_rating(),
        'review_count': route.review_count(),
        'is_favorited': is_favorited,
    }
    return render(request, 'routes/route_detail.html', context)


@login_required
def add_review(request, slug):
    """Add a review to a route."""
    route = get_object_or_404(Route, slug=slug)
    if request.method == 'POST':
        # Check if user already reviewed
        if Review.objects.filter(route=route, user=request.user).exists():
            messages.warning(request, 'You have already reviewed this route.')
            return redirect('routes:detail', slug=slug)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.route = route
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been posted!')
        else:
            messages.error(request, 'Please fix the errors below.')
    return redirect('routes:detail', slug=slug)


@login_required
def toggle_favorite(request, slug):
    """Toggle route as favorite."""
    route = get_object_or_404(Route, slug=slug)
    profile = request.user.profile
    if profile.favorite_routes.filter(pk=route.pk).exists():
        profile.favorite_routes.remove(route)
        messages.info(request, 'Removed from favorites.')
    else:
        profile.favorite_routes.add(route)
        messages.success(request, 'Added to favorites!')
    return redirect('routes:detail', slug=slug)


# ─── Admin CRUD ────────────────────────────────────────────

@staff_member_required
def route_create(request):
    """Create a new route (admin only)."""
    if request.method == 'POST':
        form = RouteForm(request.POST, request.FILES)
        if form.is_valid():
            route = form.save(commit=False)
            route.created_by = request.user
            route.save()
            form.save_m2m()
            messages.success(request, f'Route "{route.title}" created!')
            return redirect('routes:detail', slug=route.slug)
    else:
        form = RouteForm()
    return render(request, 'routes/route_form.html', {
        'form': form, 'title': 'Add New Route'
    })


@staff_member_required
def route_edit(request, slug):
    """Edit an existing route (admin only)."""
    route = get_object_or_404(Route, slug=slug)
    if request.method == 'POST':
        form = RouteForm(request.POST, request.FILES, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, f'Route "{route.title}" updated!')
            return redirect('routes:detail', slug=route.slug)
    else:
        form = RouteForm(instance=route)
    return render(request, 'routes/route_form.html', {
        'form': form, 'title': 'Edit Route', 'route': route
    })


@staff_member_required
def route_delete(request, slug):
    """Delete a route (admin only)."""
    route = get_object_or_404(Route, slug=slug)
    if request.method == 'POST':
        title = route.title
        route.delete()
        messages.success(request, f'Route "{title}" deleted.')
        return redirect('routes:list')
    return render(request, 'routes/route_confirm_delete.html', {
        'route': route
    })


def about(request):
    """About page."""
    return render(request, 'about.html')
