# OnlyPans Recipe App

A social recipe-sharing platform where users can create, discover, and share recipes, follow other cooks, and access premium content.

## Features

-   User registration, login, and profile management
-   Create, edit, and delete recipes with step-by-step instructions and photos
-   Browse and search public recipes by tags, ingredients, and more
-   Like, comment, and rate recipes
-   Follow other users and build a cooking community
-   Premium subscriptions for exclusive content
-   Recipe books for organizing and selling collections
-   Cloudinary integration for image hosting

## Project Structure

-   `recipes/` — Recipe-related models, views, and templates
-   `accounts/` — Custom user model and user-related features
-   `onlypans/` — Project settings and main URL configuration

## Getting Started

### Prerequisites

## Project Structure

-   `recipes/` — All models (Recipe, Ingredient, Unit, Tag, etc.), views, and templates
-   `onlypans/` — Project settings and main URL configuration

### Installation

## Features

-   Anyone can browse and search public recipes
-   Registered users can create, edit, and delete their own recipes
-   Recipes include step-by-step instructions, photos, and tags
-   User registration and login
-   Cloudinary integration for image hosting
    source .venv/bin/activate # On Windows: .venv\Scripts\activate
    ```

    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables in `env.py` or a `.env` file (see example below).
5. Run migrations:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
7. Start the development server:
    ```bash
    python manage.py runserver
    ```

### Example `env.py`

```python
import os
os.environ.setdefault("DATABASE_URL", "your_postgres_url")
os.environ.setdefault("SECRET_KEY", "your_secret_key")
os.environ.setdefault("CLOUDINARY_URL", "your_cloudinary_url")
```

## Contributing

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/TBragg88/only_pans_project.git
    cd only_pans_project
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables in `env.py` or a `.env` file (see example below).
5. Run migrations:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser (for admin access):
    ```bash
    python manage.py createsuperuser
    ```
7. Start the development server:
    ```bash
    python manage.py runserver
    ```
    Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Acknowledgements

-   Django
-   Cloudinary
-   dbdiagram.io for ERD
-   All contributors and testers
