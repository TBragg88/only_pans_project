# recipes/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import (Recipe, RecipeIngredient, RecipeStep, Tag, Ingredient, 
                     Unit, Comment, Rating)


class RecipeForm(forms.ModelForm):
    """Main recipe form"""
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'cook_time', 'servings', 'image', 'image_url', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recipe title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of your recipe'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Prep time in minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Cook time in minutes'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of servings'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Or enter image URL'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Group tags by type for better display
        self.fields['tags'].queryset = Tag.objects.all().order_by('tag_type', 'name')


class RecipeIngredientForm(forms.ModelForm):
    """Form for individual recipe ingredients"""
    
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit', 'notes']
        widgets = {
            'ingredient': forms.Select(attrs={
                'class': 'form-control ingredient-select',
                'data-placeholder': 'Select an ingredient'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',
                'step': '0.1',
                'min': '0'
            }),
            'unit': forms.Select(attrs={
                'class': 'form-control unit-select'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Notes (optional)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.all().order_by('name')
        self.fields['unit'].queryset = Unit.objects.all().order_by('name')
        self.fields['ingredient'].empty_label = "Select ingredient..."
        self.fields['unit'].empty_label = "Select unit..."

    def clean(self):
        cleaned_data = super().clean()
        ingredient = cleaned_data.get('ingredient')
        quantity = cleaned_data.get('quantity')
        unit = cleaned_data.get('unit')
        
        # Only validate if this form has data (not a blank extra form)
        if ingredient or quantity or unit:
            if not ingredient:
                raise forms.ValidationError("Please select an ingredient.")
            if not quantity:
                raise forms.ValidationError("Please enter a quantity.")
            if not unit:
                raise forms.ValidationError("Please select a unit.")
        
        return cleaned_data


class RecipeStepForm(forms.ModelForm):
    """Form for individual recipe steps"""
    
    class Meta:
        model = RecipeStep
        fields = ['instruction', 'image']
        widgets = {
            'instruction': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this step...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }


class CommentForm(forms.ModelForm):
    """Form for recipe comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts about this recipe...'
            })
        }


class RatingForm(forms.ModelForm):
    """Form for rating recipes"""
    
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'step': '1'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].required = True


# Create formsets for dynamic adding of ingredients and steps
RecipeIngredientFormSet = inlineformset_factory(
    Recipe, 
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,  # Start with just 1 empty ingredient form
    can_delete=True,
    min_num=1,  # Require at least 1 ingredient
    validate_min=True,
)

RecipeStepFormSet = inlineformset_factory(
    Recipe,
    RecipeStep,
    form=RecipeStepForm,
    extra=1,  # Start with just 1 empty step form
    can_delete=True,
    min_num=1,  # Require at least 1 step
    validate_min=True,
)


class RecipeSearchForm(forms.Form):
    """Advanced search and filtering form for recipes"""
    
    # Search query
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search recipes, ingredients, or descriptions...'
        })
    )
    
    # Tags filter
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    # Cuisine type filter (based on tags with type 'cuisine')
    cuisine = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(tag_type='cuisine'),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    # Dietary restrictions filter
    dietary = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(tag_type='dietary'),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    # Time filters
    max_prep_time = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max prep time (minutes)'
        })
    )
    
    max_cook_time = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max cook time (minutes)'
        })
    )
    
    max_total_time = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max total time (minutes)'
        })
    )
    
    # Servings filter
    min_servings = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min servings'
        })
    )
    
    max_servings = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max servings'
        })
    )
    
    # Difficulty filter (based on cook time as proxy)
    DIFFICULTY_CHOICES = [
        ('', 'Any Difficulty'),
        ('easy', 'Easy (under 30 min total)'),
        ('medium', 'Medium (30-60 min total)'),
        ('hard', 'Hard (over 60 min total)'),
    ]
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    # Sorting options
    SORT_CHOICES = [
        ('-created_at', 'Newest First'),
        ('created_at', 'Oldest First'),
        ('title', 'Title A-Z'),
        ('-title', 'Title Z-A'),
        ('-average_rating', 'Highest Rated'),
        ('total_time', 'Quickest First'),
        ('-total_time', 'Longest First'),
        ('servings', 'Fewest Servings'),
        ('-servings', 'Most Servings'),
    ]
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )