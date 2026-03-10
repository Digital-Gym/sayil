from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Hiking route category (e.g., Mountain, Forest, Coastal)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=10, default='🏔️',
        help_text='Emoji icon for the category'
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Route(models.Model):
    """A hiking route with details and metadata."""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Qiyin'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default='moderate'
    )
    distance_km = models.DecimalField(
        max_digits=6, decimal_places=2,
        help_text='Distance in kilometers'
    )
    elevation_gain = models.IntegerField(
        help_text='Elevation gain in meters'
    )
    estimated_duration = models.CharField(
        max_length=50,
        help_text='e.g., "2-3 hours"'
    )
    location = models.CharField(max_length=200)
    cover_image = models.ImageField(
        upload_to='routes/covers/', blank=True, null=True
    )
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='routes'
    )
    categories = models.ManyToManyField(
        Category, related_name='routes', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while Route.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('routes:detail', kwargs={'slug': self.slug})

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(
                avg=models.Avg('rating')
            )['avg'], 1)
        return 0

    def review_count(self):
        return self.reviews.count()

    def __str__(self):
        return self.title


class Review(models.Model):
    """User review/rating for a hiking route."""
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text='Rating from 1 to 5 stars'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['route', 'user']

    def __str__(self):
        return f'{self.user.username} - {self.route.title} ({self.rating}★)'
