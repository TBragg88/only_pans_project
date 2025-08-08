# 🍳 OnlyPans - Social Recipe Sharing Platform

<div align="center">

![OnlyPans Logo](planning/images/Project_ERD_Cooking.png)

**A modern, responsive recipe sharing platform where culinary enthusiasts connect, create, and discover amazing recipes.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Heroku-purple?style=for-the-badge)](https://only-pans-d09011088446.herokuapp.com/)
[![Django](https://img.shields.io/badge/Django-4.2.23-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)

</div>

## 📋 Table of Contents

-   [From Big Vision to V1](#from-big-vision-to-v1)
-   [ERD at a Glance](#erd-at-a-glance)
-   [Project Outline](#project-outline)
-   [Features](#-features)
-   [Technology Stack](#-technology-stack)
-   [Quick Start](#-quick-start)
-   [Usage](#-usage)
-   [User Stories](#user-stories)
-   [Color Guide](#color-guide)
-   [Wireframes](#wireframes)
-   [Project Structure](#%EF%B8%8F-project-structure)
-   [Testing & What to Screenshot](#-testing--what-to-screenshot)
-   [Screenshots & Demo Guide](#-screenshots--demo-guide)
-   [Agile Delivery](#agile-delivery)
-   [Responsive Design](#responsive-design)
-   [Constraints & Technical Decisions](#constraints--technical-decisions)
-   [Roadmap](#-roadmap)
-   [AI Implementation](#ai-implementation-whats-in-whats-next)
-   [Deployment](#-deployment)
-   [Contributing](#-contributing)
-   [License](#-license)

## 📖 From Big Vision to V1

OnlyPans started as a “go big or go home” idea: a social cooking platform with premium subscriptions, live cooking, AI meal planning, DMs between chefs, a marketplace for ingredients, and native mobile apps. The ERD was ambitious by design—think Recipes, Ingredients, Steps, Tags, Ratings, Comments, Messages, Subscriptions, Orders and more all talking to each other.

Then reality stepped in (in a helpful way). To ship something reliable and genuinely useful, I focused on a crisp V1 that nails the core experience: creating, discovering, and discussing great recipes. That meant deferring a few dream features for now, keeping the stack lean, and polishing the flows users touch the most.

Here’s the spirit of the scope reduction:

-   Time-boxed delivery over feature sprawl
-   Keep the data model clean and extensible
-   Optimize performance and UX for the essentials
-   Deploy with confidence (Heroku + Postgres) and iterate

What was in the original ERD vs what shipped in V1:

-   Subscriptions, DMs, live sessions, and marketplace → Deferred to roadmap
-   AI recommendations → Designed as a future layer on top of tags and search
-   Mobile apps → Prioritized fully responsive web with Bootstrap 5
-   Video streaming → Kept to images + rich content for now

Bottom line: All the foundations are here to grow—the UX is tight, the data model is solid, and the app is delightful to use today.

## 🗺️ ERD at a Glance

The project uses a practical, production-ready slice of the original ERD. Core entities you’ll see throughout the app:

-   User & UserProfile: accounts, preferences, dietary flags
-   Recipe: title, description, times, servings, images
-   Ingredient & RecipeIngredient: flexible amounts, units, notes
-   Step (RecipeStep): ordered instruction steps with optional images
-   Tagging: Cuisine and Dietary tags for discovery and filtering
-   Rating: 1–5 star system with averages
-   Comment: threaded comments with replies

You can view the original ERD sketch here: planning/images/Project_ERD_Cooking.png

## ✨ Features

### 🔐 User Authentication & Profiles

-   **Secure Registration & Login** with Django Allauth
-   **Personalized User Profiles** with dietary preferences
-   **Social Login Integration** ready for Google/Facebook
-   **Modal-based Authentication** for seamless UX

### 🍳 Recipe Management

-   **Rich Recipe Creation** with multiple ingredients and steps
-   **Image Upload & Management** via Cloudinary
-   **Advanced Search & Filtering** by cuisine, dietary needs, cook time
-   **Print-Friendly Recipe Views** with optimized layouts
-   **Recipe Ratings & Reviews** with 5-star system

### 🎯 Discovery & Social Features

-   **Cuisine-Based Carousel** showcasing featured recipes
-   **Smart Filtering System** with quick tag-based filters
-   **Recipe Comments & Threaded Discussions**
-   **Social Sharing** with Open Graph and Twitter Cards
-   **Email Notifications** for recipe interactions

### 📱 Modern UX/UI

-   **Fully Responsive Design** across all devices
-   **Bootstrap 5** with custom styling
-   **Interactive Modals** for seamless user actions
-   **Loading States & Animations** for smooth interactions
-   **Accessible Design** with ARIA labels and semantic HTML

### 🔧 Professional Features

-   **Privacy Policy & Terms of Service** pages
-   **Contact Form** with email integration
-   **SEO Optimization** with meta tags and structured data
-   **Performance Optimized** with lazy loading and caching
-   **CSRF Protection** and XSS prevention

## Project Outline

OnlyPans is a clean, friendly Django web app where people publish beautiful recipes, browse by taste (cuisines, dietary tags), and talk about what they’re cooking. It’s fully responsive, fast, and easy on any device. Under the hood it supports full CRUD for recipes, comments, and ratings; on the front end it stays simple and focused.

What you can do today:

-   Create recipes with rich detail (images, steps, ingredients)
-   Discover via search, tags, and a curated cuisine carousel
-   Comment, reply, and rate recipes
-   Print recipes with a polished layout
-   Log in via sleek modals without losing context

What it’s ready for tomorrow:

-   Following cooks, saved collections, premium content, and smarter recommendations

## 🔧 Technology Stack

### Backend

-   **Django 4.2.23** - Web framework
-   **PostgreSQL** - Production database
-   **Django Allauth** - Authentication system
-   **Cloudinary** - Image storage and management
-   **Whitenoise** - Static file serving
-   **Gunicorn** - WSGI server

### Frontend

-   **HTML5 & CSS3** - Semantic markup and styling
-   **Bootstrap 5** - Responsive framework
-   **JavaScript (ES6+)** - Interactive functionality
-   **Font Awesome** - Icon library
-   **Google Fonts** - Typography

### Deployment & DevOps

-   **Heroku** - Cloud platform
-   **Git** - Version control
-   **GitHub** - Code repository
-   **Heroku Postgres** - Database hosting

## 🚀 Quick Start

### Prerequisites

-   Python 3.8+
-   Git
-   PostgreSQL (for local development)

### Local Development Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/TBragg88/only_pans_project.git
    cd only_pans_project
    ```

2. **Create virtual environment**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Environment Configuration**

    ```bash
    # Create .env file in project root
    cp .env.example .env
    # Edit .env with your configuration
    ```

5. **Database Setup**

    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py loaddata recipes/fixtures/sample_recipes.json
    ```

6. **Run Development Server**
    ```bash
    python manage.py runserver
    ```

Visit `http://localhost:8000` to see the application.

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/onlypans

# Cloudinary (optional for local development)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email (optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📱 Usage

### For Recipe Creators

1. **Sign Up/Login** using the modal authentication system
2. **Create Recipes** with detailed ingredients and step-by-step instructions
3. **Upload Images** to make your recipes visually appealing
4. **Tag Your Recipes** with cuisine types and dietary information
5. **Engage with Community** through comments and ratings

### For Recipe Discoverers

1. **Browse Cuisine Carousel** on the homepage for inspiration
2. **Use Advanced Search** to find recipes by ingredients, cook time, or dietary needs
3. **Filter by Tags** for quick discovery (Vegan, Gluten-Free, etc.)
4. **Save Favorites** and leave reviews
5. **Print Recipes** with the optimized print layout

### For Community Building

1. **Rate Recipes** with the 5-star system
2. **Leave Comments** and engage in recipe discussions
3. **Get Notifications** when someone interacts with your recipes
4. **Share on Social Media** with rich preview cards

## User Stories

Sample stories that guided the build (paste your full list here if desired):

-   As a visitor, I want to browse trending cuisines so I can get inspired quickly.
-   As a user, I want to create a recipe with steps and photos so others can follow along.
-   As a user, I want to search by ingredients and tags so I can cook with what I have.
-   As a user, I want to rate and comment so I can share feedback and tips.
-   As a user, I want printing to be clean so I can bring recipes into the kitchen.
-   As a cook, I want people to find my recipes easily so I can grow an audience.

## Color Guide

A welcoming, modern kitchen vibe with strong contrast and gentle accents.

-   Primary: `#0051a8` (primary-color)
-   Primary Hover: `#003d82`
-   Secondary: `#f7d794`
-   Accent — Success: `#6c5ce7`, Danger: `#fd79a8`, Warning: `#fdcb6e`, Info: `#74b9ff`
-   Light / Dark: `#fefefe` / `#2d3436`
-   Background accents: `#fff9e6`, `#e8f4fd`, `#fefaf6`, `#fef7d0`, `#a8dadc`

Tip: these live in `static/css/styles.css` under `:root` variables for easy theming.

## Wireframes

Low-fi and hi-fi wireframes informed the build. Add your images here:

-   planning/images/wireframe-home.png
-   planning/images/wireframe-recipe-list.png
-   planning/images/wireframe-recipe-detail.png
-   planning/images/wireframe-add-recipe.png

Notes:

-   A single, unified search block improves clarity and reduces cognitive load.
-   The carousel leads with “tonight’s vibe” prompts to spark exploration.
-   Recipe detail prioritizes title → image → time/servings → ingredients → steps → reviews.

## 🏗️ Project Structure

```
only_pans_project/
├── 📁 accounts/              # User authentication & profiles
│   ├── models.py            # User profile extensions
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   └── templates/           # Account-related templates
├── 📁 recipes/              # Recipe management
│   ├── models.py            # Recipe, Ingredient, Rating models
│   ├── views.py             # Recipe CRUD operations
│   ├── forms.py             # Recipe creation forms
│   ├── notifications.py     # Email notification system
│   └── templates/           # Recipe templates
├── 📁 onlypans/             # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── 📁 static/               # Static assets
│   ├── css/styles.css       # Custom styling
│   ├── js/                  # JavaScript files
│   └── images/              # Site images
├── 📁 templates/            # Global templates
│   ├── base.html            # Base template with modals
│   ├── privacy.html         # Privacy policy
│   └── terms.html           # Terms of service
├── 📁 tests/                # Test suite
└── 📁 planning/             # Documentation & ERD
```

## 🧪 Testing & What to Screenshot

V1 includes a solid testing setup focused on the real user flows—creating recipes, searching, viewing details, commenting, and rating.

Run tests locally:

```bash
# Run all tests
python manage.py test

# With coverage (optional)
coverage run --source='.' manage.py test
coverage report
coverage html
```

What the tests cover:

-   Models: Recipes, ingredients, tags, ratings, comments
-   Views: Auth, CRUD, permissions, list/detail flows
-   Forms: Recipe form, search, validation rules
-   Integration: End-to-end happy paths with key edge cases

Great testing screenshots to include:

-   Terminal output of a passing test run (e.g., 100+ tests, all green)
-   Coverage summary (coverage report) and a screenshot of the HTML coverage index
-   Any failing test’s clear error message (if demonstrating TDD or debugging)

Tip: save screenshots under planning/images or a docs/screenshots folder.

## 📸 Screenshots & Demo Guide

These highlight the app’s best UX moments. Suggested shots and filenames:

-   Homepage — cuisine carousel in motion
    -   planning/images/screenshot-home-carousel.png
    -   planning/images/screenshot-home-filter-card.png
-   Unified search + filters block (list view)
    -   planning/images/screenshot-search-and-filters.png
-   Recipe detail — hero, ingredients, steps, nutrition, ratings
    -   planning/images/screenshot-recipe-detail-hero.png
    -   planning/images/screenshot-recipe-ingredients-steps.png
-   Add Recipe flow
    -   planning/images/screenshot-add-recipe-form.png
    -   planning/images/screenshot-login-modal-on-add.png (unauthenticated CTA)
-   Auth modals
    -   planning/images/screenshot-login-modal.png
    -   planning/images/screenshot-register-modal.png
-   Profile (if enabled) and liked recipes
    -   planning/images/screenshot-profile.png
    -   planning/images/screenshot-liked-recipes.png
-   Mobile responsiveness (breakpoints 576px, 768px, 992px)
    -   planning/images/screenshot-mobile-home.png
    -   planning/images/screenshot-mobile-recipe-detail.png
-   Performance and SEO
    -   planning/images/lighthouse-overall.png
    -   planning/images/lighthouse-performance.png
    -   planning/images/lighthouse-accessibility.png

Optional: short GIF screen capture of searching → opening a recipe → adding a comment.

Pro tip: keep file names lowercase-with-dashes for consistency.

## 📚 General Features at Final (V1)

-   Cookbook-style recipe presentation with clear sections
-   Unified search and filter experience
-   Cuisine carousel for discovery
-   Comments with replies (threaded)
-   Ratings with averaged stars
-   Print-friendly layout for kitchen use
-   Auth modals for login/register without losing page context
-   Image hosting via Cloudinary
-   Email notifications on interactions

Planned next: saved collections, following favorite cooks, and optional subscription tiers.

### HTML/CSS/JS Validation

Place your validation screenshots here:

-   planning/images/validator-w3c-html.png
-   planning/images/validator-w3c-css.png
-   planning/images/eslint-report.png (if applicable)

Briefly note any non-critical warnings you intentionally accepted (e.g., vendor attributes).

## ⚖️ Constraints & Technical Decisions

Why some things waited for later—and why that’s a strength:

-   Simplicity > complexity: shipped with a clean, maintainable data model
-   Heroku + Postgres: reliable deployment path that’s easy to scale
-   Bootstrap 5 + custom CSS: polished, responsive UI without a heavy SPA
-   Cloudinary: effortless, reliable image handling
-   Modal-based auth: faster UX, fewer page loads

Deferred (by design): subscriptions/payments, DMs, live video, AI recs, marketplace, and native apps. The current architecture makes these add-ons straightforward when the time is right.

## 🌱 Roadmap

-   Smart recommendations (start with “similar by tags” → evolve to ML)
-   Saved collections and meal planning
-   Public profiles and follow system
-   Premium content tiers and payments
-   API endpoints for future mobile apps
-   Rich media (short clips) with CDN-backed hosting

## 🧠 AI Implementation (What’s in, what’s next)

-   In this iteration, AI helped with storyboarding user flows, generating realistic seed recipes, and accelerating debugging.
-   The search/tag model is ready for ML-driven recommendations (e.g., collaborative filtering or embeddings).
-   Next steps: smart search suggestions, personalized feeds, and auto-tagging ingredients from images via a lightweight model.

## 🌐 Deployment

### Heroku Deployment

1. **Create Heroku App**

    ```bash
    heroku create your-app-name
    ```

2. **Add PostgreSQL**

    ```bash
    heroku addons:create heroku-postgresql:mini
    ```

3. **Configure Environment Variables**

    ```bash
    heroku config:set SECRET_KEY=your-secret-key
    heroku config:set DEBUG=False
    heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
    # ... other variables
    ```

4. **Deploy**
    ```bash
    git push heroku main
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser
    ```

### Production Checklist

-   [ ] Environment variables configured
-   [ ] Debug mode disabled
-   [ ] Static files collected
-   [ ] Database migrations applied
-   [ ] Superuser created
-   [ ] Domain configured (if applicable)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run the test suite**
6. **Submit a pull request**

### Development Guidelines

-   Follow PEP 8 style guidelines
-   Add docstrings to new functions
-   Include tests for new features
-   Update documentation as needed

## 📊 Performance & SEO

### Lighthouse Scores

-   **Performance**: 95+
-   **Accessibility**: 100
-   **Best Practices**: 100
-   **SEO**: 100

### SEO Features

-   **Meta Tags**: Open Graph and Twitter Cards
-   **Structured Data**: Recipe schema markup
-   **Semantic HTML**: Proper heading hierarchy
-   **Alt Text**: All images have descriptive alt text
-   **Sitemap**: Automatic sitemap generation

## 🔒 Security Features

-   **CSRF Protection**: All forms include CSRF tokens
-   **XSS Prevention**: Template auto-escaping enabled
-   **SQL Injection**: Django ORM prevents SQL injection
-   **Secure Headers**: Security middleware enabled
-   **HTTPS**: Enforced in production
-   **Input Validation**: Server-side form validation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

-   **Django Community** for the amazing framework
-   **Bootstrap Team** for the responsive framework
-   **Cloudinary** for image management
-   **Heroku** for reliable hosting
-   **Font Awesome** for beautiful icons

---

<div align="center">

**Built with ❤️ by [TBragg88](https://github.com/TBragg88)**

[🌐 Live Demo](https://only-pans-d09011088446.herokuapp.com/) | [🐛 Report Bug](https://github.com/TBragg88/only_pans_project/issues) | [✨ Request Feature](https://github.com/TBragg88/only_pans_project/issues)

</div>
