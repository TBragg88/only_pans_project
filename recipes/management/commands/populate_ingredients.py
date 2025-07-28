import json
from yourapp.models import Ingredient  # Replace 'yourapp' with your actual app name

# Complete ingredient data with ALL nutritional fields
# Format: (name, category, unit, dietary_flags_list, calories, protein, carbs, fat, fiber, sugars, sodium_mg, sat_fat)
ingredients_data = [
    # Produce
    ('Carrots', 'produce', 'grams', [], 41, 0.9, 9.6, 0.2, 2.8, 4.7, 69, 0.04),
    ('Onions', 'produce', 'grams', [], 40, 1.1, 9.3, 0.1, 1.7, 4.2, 4, 0.04),
    ('Garlic', 'produce', 'grams', [], 149, 6.4, 33, 0.5, 2.1, 1, 17, 0.09),
    ('Tomatoes', 'produce', 'grams', [], 18, 0.9, 3.9, 0.2, 1.2, 2.6, 5, 0.03),
    ('Potatoes', 'produce', 'grams', [], 77, 2.0, 17, 0.1, 2.2, 0.8, 6, 0.03),
    ('Bell Peppers', 'produce', 'grams', [], 31, 1.0, 7, 0.3, 2.5, 4.2, 4, 0.07),
    ('Spinach', 'produce', 'grams', [], 23, 2.9, 3.6, 0.4, 2.2, 0.4, 79, 0.06),
    ('Broccoli', 'produce', 'grams', [], 34, 2.8, 7, 0.4, 2.6, 1.5, 33, 0.06),
    ('Mushrooms', 'produce', 'grams', [], 22, 3.1, 3.3, 0.3, 1.0, 2.0, 5, 0.05),
    ('Lettuce', 'produce', 'grams', [], 15, 1.4, 2.9, 0.2, 1.3, 0.8, 28, 0.03),
    ('Green Onions', 'produce', 'stalks', [], 32, 1.8, 7.3, 0.2, 2.6, 2.3, 16, 0.03),
    ('Romaine Lettuce', 'produce', 'heads', [], 17, 1.2, 3.3, 0.3, 2.1, 1.2, 8, 0.02),
    ('Chives', 'herbs', 'tablespoons', [], 30, 0.9, 0.7, 0.1, 0.5, 0.1, 3, 0.01),
    ('Parsley', 'herbs', 'grams', [], 36, 3, 6, 0.8, 3.3, 0.9, 56, 0.1),
    ('Avocado', 'produce', 'grams', [], 160, 2, 9, 15, 7, 0.7, 7, 2.1),
    ('Sweet Potato', 'produce', 'grams', [], 86, 1.6, 20, 0.1, 3, 4.2, 55, 0.02),
    ('Zucchini', 'produce', 'grams', [], 17, 1.2, 3.1, 0.3, 1, 2.5, 8, 0.1),
    ('Cucumber', 'produce', 'grams', [], 16, 0.7, 3.6, 0.1, 0.5, 1.7, 2, 0.04),
    ('Apple', 'produce', 'grams', [], 52, 0.3, 14, 0.2, 2.4, 10, 1, 0.03),
    ('Lemon', 'produce', 'grams', [], 29, 1.1, 9.3, 0.3, 2.8, 2.5, 2, 0.04),
    ('Lime', 'produce', 'grams', [], 30, 0.7, 11, 0.2, 2.8, 1.7, 2, 0.02),
    ('Strawberry', 'produce', 'grams', [], 32, 0.7, 7.7, 0.3, 2, 4.9, 1, 0.02),
    ('Blueberry', 'produce', 'grams', [], 57, 0.7, 14, 0.3, 2.4, 10, 1, 0.03),
    ('Corn', 'produce', 'grams', [], 86, 3.2, 19, 1.2, 2.7, 6.3, 15, 0.2),
    ('Peas', 'produce', 'grams', [], 81, 5, 14, 0.4, 5, 5.7, 5, 0.1),
    ('Mango', 'produce', 'grams', [], 60, 0.8, 15, 0.4, 1.6, 13.7, 1, 0.1),
    ('Pineapple', 'produce', 'grams', [], 50, 0.5, 13, 0.1, 1.4, 9.9, 1, 0.1),
    ('Watermelon', 'produce', 'grams', [], 30, 0.6, 8, 0.2, 0.4, 6.2, 1, 0.1),
    ('Grapes', 'produce', 'grams', [], 69, 0.7, 18, 0.2, 0.9, 15, 2, 0.1),
    ('Cherries', 'produce', 'grams', [], 50, 1, 12, 0.3, 1.6, 8, 1, 0.1),
    ('Pears', 'produce', 'grams', [], 57, 0.4, 15, 0.1, 3.1, 10, 1, 0.1),
    ('Figs', 'produce', 'grams', [], 74, 0.8, 19, 0.3, 2.9, 16, 1, 0.1),
    ('Dates', 'produce', 'grams', [], 282, 2.5, 75, 0.4, 8, 63, 1, 0.1),
    ('Pomegranate', 'produce', 'grams', [], 83, 1.7, 19, 1.2, 4, 14, 3, 0.1),
    ('Artichoke', 'produce', 'grams', [], 47, 3.3, 11, 0.2, 5.4, 1, 94, 0.1),
    ('Eggplant', 'produce', 'grams', [], 25, 1, 6, 0.2, 3, 3.5, 2, 0.1),
    ('Cauliflower', 'produce', 'grams', [], 25, 1.9, 5, 0.3, 2, 1.9, 30, 0.1),
    ('Kale', 'produce', 'grams', [], 49, 4.3, 9, 0.9, 3.6, 1.6, 38, 0.1),
    ('Arugula', 'produce', 'grams', [], 25, 2.6, 3.7, 0.7, 1.6, 2, 27, 0.1),
    ('Radish', 'produce', 'grams', [], 16, 0.7, 3.4, 0.1, 1.6, 1.9, 39, 0.1),
    ('Turnip', 'produce', 'grams', [], 28, 0.9, 6.4, 0.1, 1.8, 3.8, 67, 0.1),
    ('Rutabaga', 'produce', 'grams', [], 37, 1.1, 8.6, 0.2, 2.3, 4.5, 12, 0.1),
    ('Parsnip', 'produce', 'grams', [], 75, 1.2, 18, 0.3, 4.9, 4.8, 10, 0.1),
    ('Leeks', 'produce', 'grams', [], 61, 1.5, 14, 0.3, 1.8, 3.9, 20, 0.1),
    ('Fennel', 'produce', 'grams', [], 31, 1.2, 7, 0.2, 3.1, 3.9, 52, 0.1),
    ('Okra', 'produce', 'grams', [], 33, 2, 7, 0.2, 3.2, 1.5, 7, 0.1),
    ('Bok Choy', 'produce', 'grams', [], 13, 1.5, 2.2, 0.2, 1, 1.2, 65, 0.1),
    ('Daikon', 'produce', 'grams', [], 18, 0.6, 4.1, 0.1, 1.6, 2.5, 21, 0.1),
    ('Jicama', 'produce', 'grams', [], 38, 0.7, 9, 0.1, 4.9, 1.8, 4, 0.1),
    
    # Meat & Protein
    ('Chicken Breast', 'meat', 'grams', [], 165, 31, 0, 3.6, 0, 0, 74, 1.0),
    ('Ground Beef', 'meat', 'grams', [], 250, 26, 0, 15, 0, 0, 78, 6.1),
    ('Salmon', 'fish', 'grams', [], 208, 22, 0, 12, 0, 0, 48, 1.9),
    ('Eggs', 'protein', 'pieces', [], 155, 13, 1.1, 11, 0, 0.7, 124, 3.1),
    ('Bacon', 'meat', 'grams', [], 541, 37, 1.4, 42, 0, 0, 1717, 13.5),
    ('Anchovies', 'fish', 'fillets', [], 210, 29, 0, 10, 0, 0, 3660, 2.3),
    ('Tuna', 'fish', 'grams', [], 132, 28, 0, 0.6, 0, 0, 50, 0.2),
    ('Pork Chop', 'meat', 'grams', [], 231, 25, 0, 14, 0, 0, 59, 5.2),
    ('Turkey Breast', 'meat', 'grams', [], 135, 30, 0, 1, 0, 0, 50, 0.3),
    ('Shrimp', 'fish', 'grams', [], 99, 24, 0.2, 0.3, 0, 0, 111, 0.1),
    ('Ham', 'meat', 'grams', [], 145, 20, 1.5, 6, 0, 1.5, 1200, 2.1),
    ('Tofu', 'protein', 'grams', [], 76, 8, 1.9, 4.8, 0.3, 0.6, 7, 0.7),
    ('Tempeh', 'protein', 'grams', [], 192, 20, 7.6, 11, 1.4, 0.5, 9, 2.2),
    ('Seitan', 'protein', 'grams', ['gluten'], 370, 75, 14, 1.9, 1.2, 0.5, 30, 0.2),
    ('Jackfruit', 'produce', 'grams', [], 95, 2.5, 23, 0.6, 1.5, 19, 3, 0.1),
    ('Edamame', 'protein', 'grams', ['soy'], 121, 11, 10, 5, 5.2, 2.2, 6, 0.6),
    ('Plant-Based Ground Meat', 'protein', 'grams', [], 250, 18, 9, 15, 3, 1, 400, 6),
    ('Plant-Based Sausage', 'protein', 'grams', [], 270, 20, 8, 18, 2, 1, 500, 7),
    
    # Dairy
    ('Milk', 'dairy', 'ml', ['dairy'], 64, 3.2, 4.8, 3.6, 0, 5.1, 44, 2.3),
    ('Butter', 'dairy', 'grams', ['dairy'], 717, 0.9, 0.1, 81, 0, 0.1, 11, 51),
    ('Cheddar Cheese', 'dairy', 'grams', ['dairy'], 403, 25, 1.3, 33, 0, 0.5, 653, 21),
    ('Parmesan Cheese', 'dairy', 'grams', ['dairy'], 431, 38, 4, 29, 0, 0, 1529, 19),
    ('Yogurt', 'dairy', 'grams', ['dairy'], 61, 3.5, 4.7, 3.3, 0, 4.7, 36, 2.1),
    ('Heavy Cream', 'dairy', 'ml', ['dairy'], 340, 2.8, 2.8, 36, 0, 2.9, 38, 23),
    ('Sour Cream', 'dairy', 'grams', ['dairy'], 193, 2.1, 3.4, 20, 0, 3.4, 61, 12),
    ('Cream Cheese', 'dairy', 'grams', ['dairy'], 342, 6.2, 4.1, 34, 0, 4.1, 321, 20),
    ('Feta Cheese', 'dairy', 'grams', ['dairy'], 264, 14, 4, 21, 0, 4, 917, 13),
    ('Mozzarella Cheese', 'dairy', 'grams', ['dairy'], 280, 28, 3, 17, 0, 3, 627, 10),
    ('Cottage Cheese', 'dairy', 'grams', ['dairy'], 98, 11, 3.4, 4.3, 0, 3.4, 364, 1.7),

    # Dairy Alternatives
    ('Oat Milk', 'dairy', 'ml', [], 43, 1, 7, 1, 0.8, 4, 40, 0.2),
    ('Almond Milk', 'dairy', 'ml', [], 17, 0.6, 0.7, 1.2, 0.4, 0.2, 60, 0.1),
    ('Soy Milk', 'dairy', 'ml', ['soy'], 54, 3.3, 6.3, 1.6, 0.6, 4.5, 51, 0.2),
    ('Coconut Milk', 'dairy', 'ml', [], 230, 2.3, 6, 24, 2.2, 3.3, 15, 21),
    ('Rice Milk', 'dairy', 'ml', [], 47, 0.3, 9.2, 1, 0.3, 5, 17, 0.1),
    ('Vegan Cheese', 'dairy', 'grams', [], 270, 1, 6, 23, 0, 0, 800, 18),
    ('Vegan Yogurt', 'dairy', 'grams', [], 60, 1.5, 8, 2.5, 0.5, 7, 30, 1.2),
    
    # Grains & Starches  
    ('Rice', 'grains', 'grams', [], 365, 7.1, 80, 0.7, 1.3, 0.1, 5, 0.2),
    ('Pasta', 'grains', 'grams', ['gluten'], 371, 13, 74, 1.5, 3.2, 2.7, 6, 0.3),
    ('Spaghetti', 'grains', 'grams', ['gluten'], 371, 13, 74, 1.5, 3.2, 2.7, 6, 0.3),
    ('Bread', 'grains', 'slices', ['gluten'], 265, 9, 49, 3.2, 2.7, 5.7, 491, 0.6),
    ('Baked Beans', 'canned', 'can', [], 78, 4.7, 12.9, 0.4, 3.7, 4.7, 422, 0.1),
    ('Flour', 'baking', 'grams', ['gluten'], 364, 10, 76, 1.0, 2.7, 0.3, 2, 0.2),
    ('Oats', 'grains', 'grams', [], 389, 17, 66, 7, 10.6, 0.99, 2, 1.2),
    ('Vegetable Oil', 'oils', 'tablespoons', [], 120, 0, 0, 14, 0, 0, 0, 2),
    ('Sesame Oil', 'oils', 'teaspoons', [], 40, 0, 0, 4.5, 0, 0, 0, 0.7),
    ('Quinoa', 'grains', 'grams', [], 120, 4.1, 21.3, 1.9, 2.8, 0.9, 7, 0.2),
    ('Barley', 'grains', 'grams', [], 354, 12, 73, 2.3, 17.3, 0.8, 12, 0.3),
    ('Couscous', 'grains', 'grams', [], 112, 3.8, 23, 0.2, 1.4, 0.1, 5, 0.04),
    ('Cornmeal', 'grains', 'grams', [], 370, 8, 79, 3.9, 7.3, 0.6, 7, 0.5),
    ('Buckwheat Flour', 'baking', 'grams', [], 343, 13, 71, 3.4, 10, 0.8, 11, 0.7),
    ('Rye Flour', 'baking', 'grams', ['gluten'], 325, 10, 70, 2, 15, 0.7, 2, 0.2),
    ('Spelt Flour', 'baking', 'grams', ['gluten'], 338, 15, 70, 2.4, 10.7, 0.7, 2, 0.3),
    ('Teff', 'grains', 'grams', [], 347, 13, 73, 2.1, 8, 0.7, 12, 0.5),
    ('Millet', 'grains', 'grams', [], 378, 11, 73, 4.2, 8.5, 0.6, 5, 0.7),
    ('Amaranth', 'grains', 'grams', [], 371, 14, 65, 7, 7, 1.7, 4, 1.5),
    ('Sorghum', 'grains', 'grams', [], 339, 11, 72, 3.3, 6.6, 2.5, 6, 0.5),
    ('Bulgur', 'grains', 'grams', ['gluten'], 342, 12, 76, 0.4, 18, 0.2, 17, 0.1),
    ('Farro', 'grains', 'grams', ['gluten'], 340, 14, 72, 2, 10, 0.7, 5, 0.2),
    ('Freekeh', 'grains', 'grams', ['gluten'], 325, 12, 70, 2, 10, 0.7, 5, 0.2),
    ('Rice Noodles', 'grains', 'grams', [], 108, 2, 24, 0.2, 1, 0.1, 10, 0.1),
    ('Udon', 'grains', 'grams', ['gluten'], 127, 3, 27, 0.2, 1, 0.1, 10, 0.1),
    ('Soba', 'grains', 'grams', ['gluten'], 99, 5, 21, 0.1, 2, 0.1, 5, 0.1),
    ('Ramen', 'grains', 'grams', ['gluten'], 436, 10, 65, 17, 2, 0.7, 1, 7),
    ('Tortilla', 'grains', 'pieces', [], 218, 6, 35, 5, 2, 1, 467, 1.2),
    ('Naan', 'grains', 'pieces', ['gluten'], 320, 9, 60, 6, 2, 2, 400, 2.5),
    ('Pita', 'grains', 'pieces', ['gluten'], 275, 9, 55, 1, 2.4, 0, 536, 0.2),
    ('Lavash', 'grains', 'pieces', ['gluten'], 250, 8, 50, 2, 2, 0, 400, 1.5),
    ('Injera', 'grains', 'pieces', [], 166, 5, 35, 0.5, 2, 0.5, 10, 0.1),
    
    # Pantry Staples
    ('Olive Oil', 'oils', 'ml', [], 884, 0, 0, 100, 0, 0, 2, 14),
    ('Brown Sugar', 'baking', 'grams', [], 380, 0, 98, 0, 0, 97, 28, 0),
    ('White Sugar', 'baking', 'grams', [], 387, 0, 100, 0, 0, 99.8, 1, 0),
    ('Salt', 'seasonings', 'grams', [], 0, 0, 0, 0, 0, 0, 38758, 0),
    ('Black Pepper', 'spices', 'grams', [], 251, 10, 64, 3.3, 25, 0.6, 20, 1.4),
    ('Sugar', 'baking', 'grams', [], 387, 0, 100, 0, 0, 99.8, 1, 0),
    ('Honey', 'sweeteners', 'grams', [], 304, 0.3, 82, 0, 0.2, 82.4, 4, 0),
    ('Canola Oil', 'oils', 'ml', [], 884, 0, 0, 100, 0, 0, 2, 7),
    ('Sunflower Oil', 'oils', 'ml', [], 884, 0, 0, 100, 0, 0, 1, 10),
    ('Peanut Butter', 'spreads', 'grams', [], 588, 25, 20, 50, 6, 9, 17, 10),
    ('Almond Butter', 'spreads', 'grams', [], 614, 21, 20, 55, 7, 4, 1, 4),
    ('Maple Syrup', 'sweeteners', 'ml', [], 260, 0, 67, 0, 0, 60, 12, 0),
    
    # Herbs
    ('Basil', 'herbs', 'grams', [], 22, 3.2, 2.6, 0.6, 1.6, 0.3, 4, 0.04),
    ('Oregano', 'herbs', 'grams', [], 265, 9, 69, 4.3, 42.5, 4.1, 25, 1.6),
    ('Thyme', 'herbs', 'grams', [], 276, 9.1, 64, 7.4, 37, 1.7, 9, 4.9),
    ('Dill', 'herbs', 'grams', [], 43, 3.5, 7, 1.1, 2.1, 0.1, 61, 0.06),
    ('Rosemary', 'herbs', 'grams', [], 131, 3.3, 21, 5.9, 14, 0.5, 50, 2.8),
    ('Sage', 'herbs', 'grams', [], 315, 11, 61, 13, 40, 1.7, 7, 7),

    # Spices
    ('Red Pepper Flakes', 'spices', 'teaspoons', [], 6, 0.3, 1.1, 0.3, 0.5, 0.5, 1, 0.02),
    ('Paprika', 'spices', 'grams', [], 282, 14, 54, 13, 37, 10, 68, 2.1),
    ('Cumin', 'spices', 'grams', [], 375, 18, 44, 22, 11, 2.2, 168, 1.5),
    ('Garlic Powder', 'spices', 'grams', [], 331, 16, 73, 0.7, 9, 2.4, 599, 0.2),
    ('Curry Powder', 'spices', 'grams', [], 325, 14, 58, 14, 33, 2.8, 52, 2.3),
    ('Chili Powder', 'spices', 'grams', [], 282, 13, 49, 14, 30, 2.8, 77, 2.1),
    ('Cinnamon', 'spices', 'grams', [], 247, 4, 81, 1.2, 53, 2.2, 10, 0.3),
    ('Nutmeg', 'spices', 'grams', [], 525, 6, 49, 36, 21, 28, 16, 25),
    ('Cloves', 'spices', 'grams', [], 274, 6, 65, 13, 34, 2.4, 243, 4),
    ('Szechuan Peppercorn', 'spices', 'grams', [], 305, 12, 65, 7, 30, 0, 20, 1.2),
    ('Fenugreek', 'spices', 'grams', [], 323, 23, 58, 6.4, 25, 0, 67, 1.5),
    ('Asafoetida', 'spices', 'grams', [], 297, 4, 67, 1, 30, 0, 50, 0.5),
    ('Sumac', 'spices', 'grams', [], 330, 10, 70, 4, 30, 0, 40, 1.2),
    ('Za’atar', 'spices', 'grams', [], 270, 8, 55, 7, 30, 0, 40, 1.3),
    ('Berbere', 'spices', 'grams', [], 300, 10, 60, 5, 25, 0, 20, 1.0),
    ('Ras el Hanout', 'spices', 'grams', [], 320, 12, 60, 14, 30, 0, 40, 1.5),
    ('Garam Masala', 'spices', 'grams', [], 320, 12, 60, 14, 30, 0, 40, 1.5),
    ('Herbes de Provence', 'spices', 'grams', [], 250, 7, 50, 5, 30, 0, 25, 1.1),
    ('Italian Seasoning', 'spices', 'grams', [], 251, 8, 52, 6, 32, 0, 30, 1.2),
    ('Cajun Seasoning', 'spices', 'grams', [], 300, 10, 60, 5, 25, 0, 20, 1.0),
    ('Old Bay', 'spices', 'grams', [], 250, 8, 50, 5, 20, 0, 30, 1.2),
    ('Lemon Pepper', 'spices', 'grams', [], 330, 10, 70, 4, 30, 0, 40, 1.2),
    ('Montreal Steak Seasoning', 'spices', 'grams', [], 280, 8, 50, 10, 20, 0, 30, 2.0),

    # Condiments
    ('Mayonnaise', 'condiments', 'ml', [], 680, 1, 0.6, 75, 0, 0.6, 635, 12),
    ('Soy Sauce', 'condiments', 'ml', ['soy'], 8, 1.3, 0.8, 0, 0.1, 0.4, 5493, 0),
    ('Lemon Juice', 'condiments', 'ml', [], 22, 0.4, 6.9, 0.2, 0.3, 1.4, 2, 0.04),
    ('Vinegar', 'condiments', 'ml', [], 18, 0, 0.04, 0, 0, 0.04, 2, 0),
    ('Mustard', 'condiments', 'grams', [], 66, 4.4, 7.1, 3.3, 3.3, 2.8, 1135, 0.2),
    ('Fish Sauce', 'condiments', 'ml', [], 60, 0, 1, 0, 0, 1, 7650, 0),
    ('Hoisin Sauce', 'condiments', 'ml', [], 220, 3, 53, 0.7, 0.9, 34, 2730, 0),
    ('Teriyaki Sauce', 'condiments', 'ml', [], 89, 1.2, 20, 0.2, 0.3, 13, 620, 0),
    ('Sriracha', 'condiments', 'ml', [], 93, 1, 19, 0.7, 0.9, 14, 1380, 0),
    ('Harissa', 'condiments', 'ml', [], 80, 2, 10, 5, 2, 7, 1200, 1.5),
    ('Tahini', 'condiments', 'grams', [], 595, 17, 23, 53, 9.3, 0, 17, 7.5),
    ('Miso', 'condiments', 'grams', ['soy'], 199, 12, 26, 6, 5, 6, 3720, 1.2),
    ('Pesto', 'condiments', 'grams', [], 303, 6, 4, 30, 2, 1, 600, 5),
    ('Chimichurri', 'condiments', 'grams', [], 120, 1, 2, 12, 1, 1, 400, 2),
    ('Salsa Verde', 'condiments', 'grams', [], 70, 1, 4, 5, 2, 2, 500, 1),
    ('Tzatziki', 'condiments', 'grams', [], 60, 3, 2, 4, 0.5, 1, 300, 2),
    ('Hummus', 'condiments', 'grams', [], 166, 8, 14, 10, 6, 0.3, 240, 1.5),
    ('Relish', 'condiments', 'grams', [], 97, 0.6, 24, 0.1, 1.2, 20, 710, 0),
    ('Pickled Ginger', 'condiments', 'grams', [], 60, 0.3, 15, 0.1, 1, 12, 500, 0.1),

    # Baking
    ('Vanilla Extract', 'baking', 'teaspoons', [], 12, 0, 0.6, 0, 0, 0.6, 0, 0),
    ('Baking Soda', 'baking', 'teaspoons', [], 0, 0, 0, 0, 0, 0, 1259, 0),
    ('Chocolate Chips', 'baking', 'grams', [], 479, 4.5, 62, 24, 7, 52, 1, 14),
    ('Buttermilk', 'dairy', 'ml', ['dairy'], 62, 3.3, 4.8, 1, 0, 5, 50, 0.7),
    ('Sweetened Condensed Milk', 'dairy', 'ml', ['dairy'], 321, 8, 55, 8, 0, 55, 120, 5),
    ('Evaporated Milk', 'dairy', 'ml', ['dairy'], 134, 7, 10, 7, 0, 10, 100, 4),
    ('Cream of Tartar', 'baking', 'grams', [], 258, 0, 0, 0, 0, 0, 0, 0),
    ('Gelatin', 'baking', 'grams', [], 335, 85, 0, 0, 0, 0, 160, 0),
    ('Pectin', 'baking', 'grams', [], 0, 0, 0, 0, 0, 0, 0, 0),
    ('Marzipan', 'baking', 'grams', [], 451, 9, 57, 21, 3, 57, 18, 2),
    ('Fondant', 'baking', 'grams', [], 366, 0, 92, 0, 0, 92, 10, 0),
    ('Baking Powder', 'baking', 'teaspoons', [], 53, 0, 28, 0, 0, 0, 488, 0),
    ('Cornstarch', 'baking', 'tablespoons', [], 30, 0, 7, 0, 0, 0, 1, 0),
    ('Yeast', 'baking', 'grams', [], 325, 40, 41, 8, 26, 0, 40, 0.5),

    # Sweeteners
    ('Stevia', 'sweeteners', 'grams', [], 0, 0, 0, 0, 0, 0, 0, 0),
    ('Agave Syrup', 'sweeteners', 'ml', [], 310, 0, 76, 0, 0, 68, 4, 0),
    ('Coconut Sugar', 'sweeteners', 'grams', [], 375, 0, 100, 0, 0, 75, 30, 0),
    ('Date Syrup', 'sweeteners', 'ml', [], 280, 1, 75, 0, 0, 63, 10, 0),
    ('Brown Rice Syrup', 'sweeteners', 'ml', [], 316, 0, 78, 0, 0, 63, 10, 0),
    ('Monk Fruit Sweetener', 'sweeteners', 'grams', [], 0, 0, 0, 0, 0, 0, 0, 0),
    ('Erythritol', 'sweeteners', 'grams', [], 0, 0, 100, 0, 0, 0, 0, 0),
    ('Xylitol', 'sweeteners', 'grams', [], 240, 0, 100, 0, 0, 0, 0, 0),

    # nuts & seeds
    ('Pistachios', 'protein', 'grams', [], 562, 20, 28, 45, 10, 7, 1, 5.6),
    ('Hazelnuts', 'protein', 'grams', [], 628, 15, 17, 61, 10, 4, 2, 4.5),
    ('Macadamia Nuts', 'protein', 'grams', [], 718, 8, 14, 76, 9, 4, 5, 12),
    ('Pecans', 'protein', 'grams', [], 691, 9, 14, 72, 10, 4, 0, 6.2),
    ('Brazil Nuts', 'protein', 'grams', [], 659, 14, 12, 67, 8, 2, 3, 15),
    ('Pine Nuts', 'protein', 'grams', [], 673, 14, 13, 68, 4, 4, 2, 4.9),
    ('Hemp Seeds', 'protein', 'grams', [], 553, 32, 8.7, 48, 4, 1.5, 5, 4.6),
    ('Chia Seeds', 'protein', 'grams', [], 486, 17, 42, 31, 34, 0, 16, 3.3),
    ('Flax Seeds', 'protein', 'grams', [], 534, 18, 29, 42, 27, 1.6, 30, 3.7),

    # Additional Ingredients
]

print("Starting ingredient population...")

created_count = 0
existing_count = 0

for name, category, unit, dietary_flags_list, calories, protein, carbs, fat, fiber, sugars, sodium_mg, sat_fat in ingredients_data:
    # Convert dietary flags list to JSON string
    dietary_flags_json = json.dumps(dietary_flags_list)
    
    ingredient, created = Ingredient.objects.get_or_create(
        name=name,
        defaults={
            'category': category,
            'common_unit': unit,
            'dietary_flags': dietary_flags_json,
            'calories_per_100g': calories,
            'protein_per_100g': protein,
            'carbs_per_100g': carbs,
            'fat_per_100g': fat,
            'fibre_per_100g': fiber,
            'sugars_per_100g': sugars,
            'sodium_mg_per_100g': sodium_mg,
            'saturated_fat_per_100g': sat_fat,
        }
    )
    
    if created:
        created_count += 1
        print(f"✓ Created: {name}")
    else:
        existing_count += 1
        print(f"- Already exists: {name}")

print(f"\nDone! Created {created_count} new ingredients, {existing_count} already existed.")
print("Your ingredient database is now ready for recipes!")