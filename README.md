# OnlyPans Recipe App

A comprehensive social recipe-sharing platform where users can create, discover, and share recipes, build cooking communities, and access premium content. Built with Django and modern web technologies.

![OnlyPans Banner](planning/images/Project_ERD_Cooking.png)

## Table of Contents

-   [User Experience Design](#user-experience-design)
-   [Features](#features)
-   [Agile Development](#agile-development)
-   [Testing](#testing)
-   [Deployment](#deployment)
-   [Credits](#credits)
-   [AI Implementation](#ai-implementation)

## User Experience Design

### User Stories

#### As a New Visitor

-   I want to browse public recipes without creating an account so I can explore the platform
-   I want to search recipes by ingredients, cuisine, or dietary restrictions to find relevant content
-   I want to see recipe ratings and reviews to help me choose quality recipes
-   I want to easily register for an account to access more features

#### As a Registered User

-   I want to create and share my own recipes with the community
-   I want to upload photos for my recipes to make them more appealing
-   I want to save favorite recipes for easy access later
-   I want to follow other users whose recipes I enjoy
-   I want to rate and comment on recipes I've tried
-   I want to edit my profile with bio, dietary preferences, and profile picture

#### As a Recipe Creator

-   I want to organize my recipes with tags and categories
-   I want to see analytics on my recipe views and ratings
-   I want to edit or delete my published recipes
-   I want to create recipe collections or books
-   I want to control privacy settings for my recipes

#### As an Admin

-   I want to moderate user-generated content
-   I want to manage user accounts and profiles
-   I want to view platform statistics and user engagement
-   I want to manage premium features and subscriptions

### Design Principles

-   **Clean and Intuitive**: Modern, responsive design with Bootstrap 5
-   **Mobile-First**: Fully responsive design for all device sizes
-   **Accessibility**: Proper ARIA labels, semantic HTML, and keyboard navigation
-   **Performance**: Optimized images with Cloudinary and efficient database queries
-   **User-Centered**: AJAX-powered interactions for seamless user experience

## Features

### 🔐 Authentication System

-   **Custom Registration**: First name, last name, email, and username
-   **Secure Login**: AJAX-powered modals with real-time validation
-   **Profile Management**: Bio, dietary preferences, profile pictures
-   **Privacy Controls**: Toggle visibility of personal information

![Authentication Features](static/images/auth-features.png)

### 👤 User Profiles

-   **Personal Profiles**: Display user information, recipes, and statistics
-   **Recipe Portfolio**: View all user's published recipes
-   **Rating System**: Average rating calculation across all user recipes
-   **Social Features**: Follower/following counts (expandable)
-   **Dietary Preferences**: Comma-separated tags with privacy controls

![Profile Page](static/images/profile-page.png)

### 🍳 Recipe Management

-   **Rich Recipe Creation**: Title, description, ingredients, and step-by-step instructions
-   **Image Support**: Cloudinary integration for recipe and step images
-   **Tag System**: Cuisine, dietary, meal type, cooking method categorization
-   **Nutritional Data**: Ingredient-based nutritional calculations
-   **Recipe Scaling**: Adjustable serving sizes with automatic ingredient scaling

![Recipe Creation](static/images/recipe-creation.png)

### 🔍 Discovery & Search

-   **Advanced Search**: Filter by ingredients, tags, cooking time, difficulty
-   **Recipe Browse**: Paginated recipe listings with sorting options
-   **Tag Filtering**: Browse by cuisine, dietary restrictions, meal types
-   **User Discovery**: Find and follow other recipe creators

![Search Features](static/images/search-features.png)

### ⭐ Engagement Features

-   **Recipe Ratings**: 1-5 star rating system with user reviews
-   **Comments**: Threaded commenting system for recipe discussions
-   **Likes System**: Save favorite recipes for quick access
-   **Recipe Statistics**: View counts, average ratings, total ratings

### 🛡️ Admin & Moderation

-   **Enhanced Admin Interface**: Custom admin with user statistics
-   **Content Moderation**: Recipe and comment management
-   **User Management**: Profile editing and user statistics
-   **Recipe Analytics**: View counts, ratings, and engagement metrics

![Admin Interface](static/images/admin-interface.png)

### 🎨 UI/UX Features

-   **Responsive Design**: Bootstrap 5 with custom styling
-   **Toast Notifications**: Centered success/error messages
-   **AJAX Interactions**: Seamless form submissions without page reloads
-   **Loading States**: Visual feedback for user actions
-   **Hover Effects**: Interactive recipe cards and buttons

## Agile Development

This project was developed using Agile methodology with iterative development cycles.

### Project Board

The development process was managed using GitHub Projects with the following workflow:

-   **Backlog**: All user stories and features
-   **In Progress**: Currently being developed
-   **Testing**: Features under review and testing
-   **Done**: Completed and deployed features

🔗 [View Project Board](https://github.com/TBragg88/only_pans_project/projects)

### Sprint Overview

#### Sprint 1: Foundation (MVP)

-   ✅ Basic Django setup and configuration
-   ✅ User authentication system
-   ✅ Recipe model and basic CRUD operations
-   ✅ Simple recipe listing and detail views

#### Sprint 2: Enhanced User Experience

-   ✅ User profile system with image uploads
-   ✅ Enhanced authentication with AJAX modals
-   ✅ Recipe search and filtering
-   ✅ Tag system implementation

#### Sprint 3: Engagement Features

-   ✅ Rating and review system
-   ✅ Enhanced admin interface
-   ✅ Profile management with privacy controls
-   ✅ Recipe management from user profiles

#### Sprint 4: Polish & Optimization

-   ✅ Responsive design improvements
-   ✅ Performance optimizations
-   ✅ Error handling and user feedback
-   ✅ Documentation and testing

### User Story Management

User stories were tracked with the following format:

```
As a [user type], I want [functionality] so that [benefit]
```

Each story included:

-   Acceptance criteria
-   Priority (Must Have, Should Have, Could Have)
-   Story points estimation
-   Testing requirements

## Testing

### Manual Testing

#### Authentication Testing

-   ✅ User registration with all required fields
-   ✅ Email uniqueness validation
-   ✅ Username uniqueness validation
-   ✅ Password confirmation matching
-   ✅ Login with username/email
-   ✅ Logout functionality
-   ✅ Profile creation on registration

#### Profile Management Testing

-   ✅ Profile editing with image upload
-   ✅ Bio and dietary preferences updates
-   ✅ Privacy settings functionality
-   ✅ Profile viewing by other users
-   ✅ Recipe management from profile

#### Recipe Testing

-   ✅ Recipe creation with all fields
-   ✅ Image upload and display
-   ✅ Recipe editing and deletion
-   ✅ Tag system functionality
-   ✅ Search and filtering

#### UI/UX Testing

-   ✅ Responsive design on mobile/tablet/desktop
-   ✅ AJAX form submissions
-   ✅ Toast notification system
-   ✅ Loading states and error handling
-   ✅ Navigation and user flow

### Browser Compatibility

-   ✅ Chrome (latest)
-   ✅ Firefox (latest)
-   ✅ Safari (latest)
-   ✅ Edge (latest)

### Responsive Testing

-   ✅ iPhone SE (375px)
-   ✅ iPad (768px)
-   ✅ Desktop (1024px+)
-   ✅ Large screens (1440px+)

### Performance Testing

-   ✅ Page load times under 3 seconds
-   ✅ Image optimization with Cloudinary
-   ✅ Database query optimization
-   ✅ Minimal JavaScript bundle size

### Accessibility Testing

-   ✅ ARIA labels and semantic HTML
-   ✅ Keyboard navigation
-   ✅ Screen reader compatibility
-   ✅ Color contrast compliance

## Deployment

### Heroku Deployment

1. **Create Heroku App**

    ```bash
    heroku create only-pans-app
    ```

2. **Set Environment Variables**

    ```bash
    heroku config:set SECRET_KEY=your_secret_key
    heroku config:set DATABASE_URL=your_postgres_url
    heroku config:set CLOUDINARY_URL=your_cloudinary_url
    heroku config:set DEBUG=False
    ```

3. **Deploy**
    ```bash
    git push heroku main
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    ```

### Local Development Setup

1. **Clone Repository**

    ```bash
    git clone https://github.com/TBragg88/only_pans_project.git
    cd only_pans_project
    ```

2. **Create Virtual Environment**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Environment Setup**
   Create `env.py` in the root directory:

    ```python
    import os
    os.environ.setdefault("SECRET_KEY", "your_secret_key")
    os.environ.setdefault("DATABASE_URL", "sqlite:///db.sqlite3")
    os.environ.setdefault("CLOUDINARY_URL", "cloudinary://your_credentials")
    os.environ.setdefault("DEBUG", "True")
    ```

5. **Database Setup**

    ```bash
    python manage.py migrate
    python manage.py create_user_profiles  # For existing users
    python manage.py createsuperuser
    ```

6. **Run Development Server**
    ```bash
    python manage.py runserver
    ```

### Dependencies

-   Django 4.2.23
-   Cloudinary (image hosting)
-   Bootstrap 5 (frontend framework)
-   Font Awesome (icons)
-   WhiteNoise (static file serving)

## Credits

### Code and Libraries

-   **Django**: Web framework - [djangoproject.com](https://www.djangoproject.com/)
-   **Bootstrap 5**: CSS framework - [getbootstrap.com](https://getbootstrap.com/)
-   **Cloudinary**: Image hosting and optimization - [cloudinary.com](https://cloudinary.com/)
-   **Font Awesome**: Icon library - [fontawesome.com](https://fontawesome.com/)

### Development Tools

-   **dbdiagram.io**: Database ERD design - [dbdiagram.io](https://dbdiagram.io/)
-   **Visual Studio Code**: Development environment
-   **GitHub**: Version control and project management
-   **Heroku**: Deployment platform

### Educational Resources

-   **Django Documentation**: Official Django tutorials and guides
-   **MDN Web Docs**: HTML, CSS, and JavaScript references
-   **Bootstrap Documentation**: Component and utility references
-   **Stack Overflow**: Community solutions and debugging help

### Content and Media

-   **Placeholder Images**: via.placeholder.com for fallback images
-   **Sample Recipes**: Created for demonstration purposes
-   **Icons**: Font Awesome free icons
-   **Color Palette**: Custom design with Bootstrap theme

### Acknowledgments

-   Code Institute for project structure guidance
-   Django community for best practices and patterns
-   Beta testers for user feedback and bug reports
-   Accessibility guidelines from WCAG 2.1

## AI Implementation

This project leveraged AI assistance throughout the development process to enhance productivity and code quality.

### AI Tools Used

-   **GitHub Copilot**: Primary AI coding assistant
-   **Code completion and suggestions**: Real-time code generation
-   **Documentation generation**: Automated docstring creation
-   **Debugging assistance**: Error resolution and optimization

### AI-Assisted Development Areas

#### 🤖 Code Generation

-   **Model Creation**: UserProfile model with proper relationships
-   **Form Development**: Custom authentication and profile forms with validation
-   **View Logic**: AJAX-enabled authentication views with error handling
-   **Template Structure**: Responsive HTML templates with Bootstrap integration

#### 🔧 Problem Solving

-   **Database Relationships**: Proper model relationships and signals
-   **Authentication Flow**: Seamless login/logout with toast notifications
-   **Image Handling**: Cloudinary integration with fallback systems
-   **Admin Interface**: Enhanced admin with custom fields and methods

#### 📋 Documentation

-   **Code Comments**: Comprehensive docstrings and inline comments
-   **README Structure**: Organized documentation with clear sections
-   **User Stories**: Detailed user story creation and acceptance criteria
-   **API Documentation**: Clear method and function documentation

#### 🚀 Optimization

-   **Performance Improvements**: Database query optimization
-   **Error Handling**: Comprehensive try-catch blocks and user feedback
-   **Security Features**: CSRF protection and input validation
-   **Code Refactoring**: Clean, maintainable code structure

### Human-AI Collaboration Process

1. **Planning**: Human-defined requirements and user stories
2. **Implementation**: AI-assisted code generation with human review
3. **Testing**: Manual testing with AI-suggested test cases
4. **Refinement**: Iterative improvements based on user feedback
5. **Documentation**: AI-assisted documentation with human curation

### Quality Assurance

-   All AI-generated code was thoroughly reviewed and tested
-   Security implications were manually verified
-   Performance was validated through manual testing
-   User experience was human-tested and refined

The AI implementation significantly accelerated development while maintaining high code quality and following Django best practices. The collaboration between human creativity and AI efficiency resulted in a robust, well-documented application.

---

**Live Site**: [Only Pans Recipe App](https://your-heroku-app.herokuapp.com)  
**Repository**: [GitHub - OnlyPans Project](https://github.com/TBragg88/only_pans_project)  
**Developer**: TBragg88
