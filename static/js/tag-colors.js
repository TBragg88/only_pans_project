/**
 * OnlyPans Recipe App - Tag Color Management
 * Handles dynamic tag coloring for recipe list tags that don't have title attributes
 */

// Tag type mappings - these should match the database tag types and names
const tagTypeMap = {
    // Cooking Methods - Teal
    cooking_method: [
        "Air Frying",
        "Baking",
        "Braising",
        "Frying",
        "Grilling",
        "No Cook",
        "One Pot",
        "Poaching",
        "Pressure Cooking",
        "Roasting",
        "Sautéing",
        "Slow Cooking",
        "Smoking",
        "Steaming",
    ],

    // Cuisine - Red
    cuisine: [
        "American",
        "Brazilian",
        "British",
        "Caribbean",
        "Chinese",
        "French",
        "German",
        "Greek",
        "Indian",
        "Italian",
        "Japanese",
        "Korean",
        "Mediterranean",
        "Mexican",
        "Middle Eastern",
        "Moroccan",
        "Russian",
        "Spanish",
        "Thai",
        "Vietnamese",
        "asian",
        "asian-inspired",
        "baking",
        "banana",
        "beans",
        "beef",
        "bread",
        "breakfast",
        "chicken",
        "creamy",
        "dessert",
        "dinner",
        "fish",
        "healthy",
        "italian",
        "mexican",
        "pasta",
        "quick",
        "salmon",
        "stir-fry",
        "tacos",
        "vegetables",
        "vegetarian",
    ],

    // Dietary - Green
    dietary: [
        "Dairy-Free",
        "Diabetic-Friendly",
        "Gluten-Free",
        "Heart-Healthy",
        "Keto",
        "Low-Carb",
        "Low-Sodium",
        "Nut-Free",
        "Paleo",
        "Sugar-Free",
        "Vegan",
        "Vegetarian",
    ],

    // Difficulty - Orange
    difficulty: [
        "Advanced",
        "Beginner",
        "Easy",
        "Expert",
        "Intermediate",
        "Medium",
    ],

    // Meal Type - Purple
    meal_type: [
        "Appetizer",
        "Beverage",
        "Breakfast",
        "Brunch",
        "Dessert",
        "Dinner",
        "Late Night",
        "Lunch",
        "Side Dish",
        "Snack",
    ],
};

/**
 * Determine tag type based on tag text content
 */
function getTagType(tagText) {
    for (const [type, tagNames] of Object.entries(tagTypeMap)) {
        if (tagNames.includes(tagText)) {
            return type;
        }
    }
    return null; // Unknown tag type
}

/**
 * Apply color class based on tag type
 */
function applyTagColor(tagElement, tagType) {
    // Remove any existing tag type classes
    tagElement.classList.remove(
        "tag-cooking-method-js",
        "tag-cuisine-js",
        "tag-dietary-js",
        "tag-difficulty-js",
        "tag-meal-type-js"
    );

    // Add appropriate class based on tag type
    switch (tagType) {
        case "cooking_method":
            tagElement.classList.add("tag-cooking-method-js");
            break;
        case "cuisine":
            tagElement.classList.add("tag-cuisine-js");
            break;
        case "dietary":
            tagElement.classList.add("tag-dietary-js");
            break;
        case "difficulty":
            tagElement.classList.add("tag-difficulty-js");
            break;
        case "meal_type":
            tagElement.classList.add("tag-meal-type-js");
            break;
    }
}

/**
 * Color all recipe list tags
 */
function colorRecipeListTags() {
    // Find all tag elements in recipe lists (those without title attributes)
    const recipeListTags = document.querySelectorAll(
        ".recipe-tags .tag-small:not([title])"
    );

    recipeListTags.forEach((tagElement) => {
        const tagText = tagElement.textContent.trim();
        const tagType = getTagType(tagText);

        if (tagType) {
            applyTagColor(tagElement, tagType);
        }
    });
}

/**
 * Color dropdown tags as well
 */
function colorDropdownTags() {
    // Also handle tags in dropdowns
    const dropdownTags = document.querySelectorAll(
        ".dropdown-item .tag-small:not([title])"
    );

    dropdownTags.forEach((tagElement) => {
        const tagText = tagElement.textContent.trim();
        const tagType = getTagType(tagText);

        if (tagType) {
            applyTagColor(tagElement, tagType);
        }
    });
}

/**
 * Initialize tag coloring when DOM is ready
 */
function initTagColoring() {
    colorRecipeListTags();
    colorDropdownTags();
}

// Run when DOM is loaded
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTagColoring);
} else {
    initTagColoring();
}

// Also run on AJAX content updates (if any)
document.addEventListener("htmx:afterRequest", initTagColoring);
document.addEventListener("htmx:afterSettle", initTagColoring);
