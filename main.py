import recipe

def extract_number(input_string):
    match = re.match(r"(\d+\.?\d*)", input_string)
    if match:
        return float(match.group(1))
    else:
        raise ValueError("Invalid quantity. Please enter a numeric value.")

def main():
    create_tables()

    print("Add a new recipe:")
    name = input("Recipe name: ")

    while True:
        try:
            cooking_time = int(input("Cooking time (in minutes): "))
            break
        except ValueError:
            print("Invalid input. Please enter a number for cooking time.")

    instructions = input("Instructions: ")
    recipe_id = add_recipe(name, cooking_time, instructions)
    print(f"Recipe added with ID: {recipe_id}")

    print("\nAdd a new ingredient:")
    ingredient_name = input("Ingredient name: ")

    while True:
        try:
            quantity_input = input("Quantity (e.g., 1.5 or 2): ")
            quantity = extract_number(quantity_input)
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for quantity.")

    unit = input("Unit (e.g., cup, gram): ")
    add_ingredient(ingredient_name, quantity, unit)
    print("Ingredient added.")

    print("\nCreate a new meal plan:")
    date = input("Date (YYYY-MM-DD): ")
    meal_type = input("Meal type (e.g., breakfast, lunch, dinner): ")
    create_meal_plan(recipe_id, date, meal_type)
    print("Meal plan created.")
