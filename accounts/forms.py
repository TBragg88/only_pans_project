"""
Forms for user authentication and profile management.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from recipes.models import Tag


class CustomLoginForm(AuthenticationForm):
    """Custom login form with Bootstrap styling."""
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class CustomRegisterForm(forms.ModelForm):
    """Custom registration form with password confirmation."""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            })
        }

    def clean_email(self):
        """Validate that the email is available."""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered. Please use another."
            )
        return email

    def clean_username(self):
        """Validate that the username is available."""
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose another."
            )
        return username

    def clean_password2(self):
        """Validate that the two password entries match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the user with the hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information."""
    
    # Add first/last name fields from User model
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    
    # Privacy settings
    show_dietary_preferences = forms.BooleanField(
        required=False,
        initial=True,
        label='Show dietary preferences to other users',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    show_email = forms.BooleanField(
        required=False,
        initial=False,
        label='Show email address to other users',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = UserProfile
        fields = [
            'bio', 'dietary_tags', 'favorite_cuisines', 'preferred_difficulty',
            'profile_image', 'show_dietary_preferences', 'show_email'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': ('Tell us about yourself, your cooking style, '
                                'favorite cuisines, etc.')
            }),
            'dietary_tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'favorite_cuisines': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'preferred_difficulty': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'bio': 'About Me',
            'dietary_tags': 'Select Your Preferences',
            'favorite_cuisines': 'Select Your Favorites',
            'preferred_difficulty': 'Preferred Recipe Difficulty',
            'profile_image': 'Profile Picture',
        }
        help_texts = {
            'dietary_tags': ('Select all dietary restrictions that apply to '
                             'you. Recipes will be filtered accordingly.'),
            'favorite_cuisines': ('Choose cuisines you enjoy - we\'ll '
                                  'prioritize these in recommendations.'),
            'preferred_difficulty': ('Select your preferred cooking '
                                     'difficulty level for recommendations.'),
            'profile_image': 'Upload a profile picture (JPG, PNG, or GIF)',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set up tag field querysets
        self.fields['dietary_tags'].queryset = Tag.objects.filter(
            tag_type='dietary'
        ).order_by('name')
        self.fields['favorite_cuisines'].queryset = Tag.objects.filter(
            tag_type='cuisine'
        ).order_by('name')
        self.fields['preferred_difficulty'].queryset = Tag.objects.filter(
            tag_type='difficulty'
        ).order_by('name')
        
        # Add empty option for difficulty
        self.fields['preferred_difficulty'].empty_label = "No preference"
        
        if self.user:
            # Pre-populate User model fields
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        """Validate that the email is available (excluding current user)."""
        email = self.cleaned_data.get('email')
        if email and self.user:
            # Check if email exists for other users
            existing_user = User.objects.filter(email=email).exclude(
                id=self.user.id
            ).first()
            if existing_user:
                raise forms.ValidationError(
                    "This email is already registered to another user."
                )
        return email

    def save(self, commit=True):
        """Save both User and UserProfile data."""
        profile = super().save(commit=False)
        
        if self.user:
            # Update User model fields
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            
            if commit:
                self.user.save()
                profile.save()
                # Save many-to-many relationships
                self.save_m2m()
        
        return profile
