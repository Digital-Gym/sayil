from django import forms
from .models import Route, Review


class RouteForm(forms.ModelForm):
    """Form for creating and editing hiking routes."""
    class Meta:
        model = Route
        fields = [
            'title', 'description', 'difficulty', 'distance_km',
            'elevation_gain', 'estimated_duration', 'location',
            'cover_image', 'categories', 'is_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Route name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the hiking trail...',
            }),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'distance_km': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 12.5',
                'step': '0.1',
            }),
            'elevation_gain': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 500',
            }),
            'estimated_duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2-3 hours',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Chimgan Mountains',
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'categories': forms.CheckboxSelectMultiple(),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class ReviewForm(forms.ModelForm):
    """Form for submitting a review."""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience on this trail...',
            }),
        }
