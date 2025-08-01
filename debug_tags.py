#!/usr/bin/env python
"""
Debug script for tag form rendering issues
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans.settings')
django.setup()

from recipes.forms import RecipeForm
from recipes.models import Tag

print("=== Debug Tag Form Rendering ===\n")

# Test 1: Check tags in database
print("1. Tags in database:")
tags = Tag.objects.all()
print(f"   Total tags: {tags.count()}")

tag_types = {}
for tag in tags:
    if tag.tag_type not in tag_types:
        tag_types[tag.tag_type] = []
    tag_types[tag.tag_type].append(tag)

for tag_type, type_tags in tag_types.items():
    print(f"   {tag_type}: {len(type_tags)} tags")
    for tag in type_tags[:3]:  # Show first 3 tags per type
        print(f"     - {tag.name} (color: {tag.color})")
    if len(type_tags) > 3:
        print(f"     ... and {len(type_tags) - 3} more")

print()

# Test 2: Check form initialization
print("2. Form initialization:")
form = RecipeForm()
print(f"   Form tags queryset count: {form.fields['tags'].queryset.count()}")
print(f"   Form tags field type: {type(form.fields['tags'])}")
print(f"   Form tags widget type: {type(form.fields['tags'].widget)}")

print()

# Test 3: Check form choices
print("3. Form choices structure:")
choices = form.fields['tags'].choices
print(f"   Choices length: {len(list(choices))}")

# Reset choices iterator
form.fields['tags'].choices = form.fields['tags'].widget.choices
for i, (value, label) in enumerate(form.fields['tags'].choices):
    if i < 5:  # Show first 5 choices
        print(f"   Choice {i}: value={value}, label={label}")
    elif i == 5:
        print(f"   ... and {len(list(form.fields['tags'].choices)) - 5} more choices")
        break

print()

# Test 4: Check template context structure
print("4. Template context simulation:")
from django.template import Template, Context

# Simulate the queryset grouping like in template
tags_by_type = {}
for tag in Tag.objects.all().order_by('tag_type', 'name'):
    if tag.tag_type not in tags_by_type:
        tags_by_type[tag.tag_type] = []
    tags_by_type[tag.tag_type].append(tag)

print("   Tags grouped by type for template:")
for tag_type, type_tags in tags_by_type.items():
    print(f"   {tag_type}: {len(type_tags)} tags")
    print(f"     First tag: {type_tags[0].name} (id={type_tags[0].id})")

print("\n=== End Debug ===")
