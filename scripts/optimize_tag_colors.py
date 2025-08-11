#!/usr/bin/env python3
"""
Script to darken tag colors for better accessibility contrast
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append('/c/Users/tbrag/Documents/vscode-projects/django_projects/only_pans_project')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans.settings')
django.setup()

from recipes.models import Tag


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def darken_color(hex_color, factor=0.7):
    """Darken a hex color by the given factor"""
    r, g, b = hex_to_rgb(hex_color)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return rgb_to_hex((r, g, b))


def get_luminance(hex_color):
    """Calculate relative luminance of a color"""
    r, g, b = hex_to_rgb(hex_color)
    
    # Convert to relative luminance
    def relative_luminance(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4
    
    r_rel = relative_luminance(r)
    g_rel = relative_luminance(g)
    b_rel = relative_luminance(b)
    
    return 0.2126 * r_rel + 0.7152 * g_rel + 0.0722 * b_rel


def contrast_ratio(color1, color2):
    """Calculate contrast ratio between two colors"""
    lum1 = get_luminance(color1)
    lum2 = get_luminance(color2)
    
    # Ensure lighter color is numerator
    if lum1 > lum2:
        return (lum1 + 0.05) / (lum2 + 0.05)
    else:
        return (lum2 + 0.05) / (lum1 + 0.05)


def main():
    print("🎨 Tag Color Accessibility Optimizer")
    print("=====================================")
    
    tags = Tag.objects.all()
    updated_count = 0
    white = "#ffffff"
    
    for tag in tags:
        current_color = tag.color
        current_contrast = contrast_ratio(current_color, white)
        
        # WCAG AA requires 4.5:1 contrast ratio
        if current_contrast < 4.5:
            # Darken the color until we get good contrast
            darkened_color = current_color
            factor = 0.9
            
            while contrast_ratio(darkened_color, white) < 4.5 and factor > 0.3:
                factor -= 0.1
                darkened_color = darken_color(current_color, factor)
            
            if darkened_color != current_color:
                old_contrast = current_contrast
                new_contrast = contrast_ratio(darkened_color, white)
                
                print(f"Updating {tag.name} ({tag.get_tag_type_display()})")
                print(f"  {current_color} → {darkened_color}")
                print(f"  Contrast: {old_contrast:.1f}:1 → {new_contrast:.1f}:1")
                
                tag.color = darkened_color
                tag.save()
                updated_count += 1
        else:
            print(f"✓ {tag.name} ({current_color}) - Contrast: {current_contrast:.1f}:1")
    
    if updated_count > 0:
        print(f"\n🎯 Updated {updated_count} tag colors for better accessibility!")
    else:
        print(f"\n✅ All {tags.count()} tag colors already have good contrast!")


if __name__ == "__main__":
    main()
