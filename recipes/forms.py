# recipes/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient, RecipeStep, Tag, Ingredient, Unit

class RecipeForm(forms.ModelForm):
    """Main recipe form"""
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'cook_time', 'servings', 'image', 'image_url', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about this recipe...'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minutes'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of servings'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Or paste image URL (optional)'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make tags optional and group by type
        self.fields['tags'].required = False
        self.fields['tags'].queryset = Tag.objects.all().order_by('tag_type', 'name')


class RecipeIngredientForm(forms.ModelForm):
    """Form for recipe ingredients"""
    
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit', 'notes', 'order']
        widgets = {
            'ingredient': forms.Select(attrs={
                'class': 'form-select ingredient-select',
                'data-placeholder': 'Choose ingredient...'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Amount'
            }),
            'unit': forms.Select(attrs={
                'class': 'form-select',
                'data-placeholder': 'Unit...'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., diced, room temp...'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order ingredients alphabetically
        self.fields['ingredient'].queryset = Ingredient.objects.all().order_by('name')
        self.fields['unit'].queryset = Unit.objects.all().order_by('unit_type', 'name')


class RecipeStepForm(forms.ModelForm):
    """Form for recipe steps"""
    
    class Meta:
        model = RecipeStep
        fields = ['step_number', 'instruction', 'image', 'image_url']
        widgets = {
            'step_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'instruction': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this step in detail...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Or paste image URL (optional)'
            })
        }


# Create formsets for dynamic adding of ingredients and steps
RecipeIngredientFormSet = inlineformset_factory(
    Recipe, 
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=5,  # Start with 5 empty ingredient forms
    can_delete=True,
    min_num=1,  # Require at least 1 ingredient
    validate_min=True
)

RecipeStepFormSet = inlineformset_factory(
    Recipe,
    RecipeStep, 
    form=RecipeStepForm,
    extra=3,  # Start with 3 empty step forms
    can_delete=True,
    min_num=1,  # Require at least 1 step
    validate_min=True
)