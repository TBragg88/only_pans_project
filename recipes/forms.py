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
        fields = ['ingredient', 'quantity', 'unit', 'notes', 'order']
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
            }),
            'order': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.all().order_by('name')
        self.fields['unit'].queryset = Unit.objects.all().order_by('name')
        self.fields['ingredient'].empty_label = "Select ingredient..."
        self.fields['unit'].empty_label = "Select unit..."


class RecipeStepForm(forms.ModelForm):
    """Form for individual recipe steps"""
    
    class Meta:
        model = RecipeStep
        fields = ['step_number', 'instruction', 'image']
        widgets = {
            'step_number': forms.HiddenInput(),
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