# OnlyPans Static Files Organization

## Directory Structure

```
static/
├── css/
│   └── styles.css              # Master stylesheet - all project styles
├── js/
│   └── app.js                  # Main application JavaScript
└── images/                     # Project images and assets
    └── (placeholder for future assets)
```

## CSS Organization (styles.css)

The master stylesheet is organized into logical sections:

1. **CSS Variables & Root Styles** - Color scheme, spacing, transitions
2. **Base Layout & Typography** - General page layout and text styles
3. **Navigation & Header** - Navbar and navigation components
4. **Forms & Form Controls** - All form styling including dynamic forms
5. **Recipe Components** - Recipe cards, details, steps, ingredients
6. **User Profile Components** - Profile pages, avatars, stats
7. **Cards & Images** - General card components and image handling
8. **Tags & Badges** - Tag system styling with color coding
9. **Interactive Elements** - Ratings, comments, hover effects
10. **Modals & Toasts** - Modal dialogs and notification styling
11. **Utilities & Helpers** - Helper classes and utilities
12. **Responsive Design** - Mobile-first responsive breakpoints

## JavaScript Organization (app.js)

Modular JavaScript with the following functionality:

-   **Rating System** - Interactive star ratings with auto-submit
-   **Comments & Replies** - Nested comment functionality
-   **Image Previews** - File upload preview for forms
-   **Toast Notifications** - Bootstrap toast integration
-   **Modal Management** - Login/register modal switching
-   **Form Validation** - Client-side validation helpers
-   **Utility Functions** - Debouncing, loading states, etc.

## Design System

### Color Scheme

-   **Primary**: `#0d6efd` (Bootstrap blue)
-   **Secondary**: `#6c757d` (Bootstrap gray)
-   **Success**: `#28a745` (Bootstrap green)
-   **Danger**: `#dc3545` (Bootstrap red)
-   **Warning**: `#ffc107` (Bootstrap yellow)

### Component Classes

#### Recipe Components

-   `.recipe-card` - Main recipe card styling
-   `.recipe-header-image` - Hero images on recipe pages
-   `.recipe-step-number` - Numbered step indicators
-   `.recipe-ingredient-list` - Ingredient list styling

#### User Interface

-   `.tag` - Standard tag styling with color coding
-   `.tag-small` - Smaller tag variant
-   `.rating-stars` - Star rating display
-   `.comment-avatar` - User comment avatars

#### Form Components

-   `.form-container` - Main form wrapper
-   `.form-section` - Form section containers
-   `.tag-selection` - Tag selection interface
-   `.btn-add-row` / `.btn-delete-row` - Dynamic form buttons

### Responsive Breakpoints

-   **Desktop**: 1200px+
-   **Tablet**: 768px - 1199px
-   **Mobile**: < 768px

## File Guidelines

### Adding New Styles

1. Use existing CSS variables for colors and spacing
2. Follow the established section organization
3. Use semantic class names (component-based)
4. Include responsive considerations

### Adding New JavaScript

1. Add functions to the appropriate section in app.js
2. Use the established initialization pattern
3. Follow the modular approach
4. Export utilities to `window.OnlyPansApp` if needed

### Adding Images

1. Place in `/static/images/`
2. Use descriptive filenames
3. Optimize for web (WebP preferred)
4. Include alt text in templates

## Performance Notes

-   All styles concatenated into single CSS file
-   JavaScript uses efficient event delegation
-   Images should be optimized and properly sized
-   CSS uses efficient selectors and minimizes specificity conflicts

## Maintenance

-   CSS variables make theme changes easy
-   Modular JavaScript allows easy feature updates
-   Component-based approach enables consistent styling
-   Documentation helps maintain code quality
