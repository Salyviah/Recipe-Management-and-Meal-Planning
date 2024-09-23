import psycopg2

# Connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        dbname="recipe_management_meal_planning",
        user="wambui",
        password="wambui",
        host="localhost",
        port="5432"
    )

# Create the tables if they don't already exist
def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            cooking_time INTEGER NOT NULL,
            instructions TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            quantity FLOAT NOT NULL,
            unit VARCHAR(50) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS meal_plans (
            id SERIAL PRIMARY KEY,
            recipe_id INTEGER REFERENCES recipes(id),
            date DATE NOT NULL,
            meal_type VARCHAR(50) NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

# Function to add a new recipe
def add_recipe(name, cooking_time, instructions):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO recipes (name, cooking_time, instructions)
        VALUES (%s, %s, %s) RETURNING id
    """, (name, cooking_time, instructions))

    recipe_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return recipe_id

# Function to add a new ingredient
def add_ingredient(name, quantity, unit):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ingredients (name, quantity, unit)
        VALUES (%s, %s, %s)
    """, (name, quantity, unit))

    conn.commit()
    cur.close()
    conn.close()

# Function to create a new meal plan
def create_meal_plan(recipe_id, date, meal_type):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO meal_plans (recipe_id, date, meal_type)
        VALUES (%s, %s, %s)
    """, (recipe_id, date, meal_type))

    conn.commit()
    cur.close()
    conn.close()

# Function to retrieve all recipes
def view_recipes():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM recipes")
    recipes = cur.fetchall()

    print("\nAll Recipes:")
    for recipe in recipes:
        print(f"ID: {recipe[0]}, Name: {recipe[1]}, Cooking Time: {recipe[2]} minutes, Instructions: {recipe[3]}")

    cur.close()
    conn.close()

# Function to retrieve all meal plans
def view_meal_plans():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT mp.id, r.name, mp.date, mp.meal_type
        FROM meal_plans mp
        JOIN recipes r ON mp.recipe_id = r.id
    """)
    meal_plans = cur.fetchall()

    print("\nAll Meal Plans:")
    for meal_plan in meal_plans:
        print(f"Meal Plan ID: {meal_plan[0]}, Recipe: {meal_plan[1]}, Date: {meal_plan[2]}, Meal Type: {meal_plan[3]}")

    cur.close()
    conn.close()

# Function to delete a recipe
def delete_recipe(recipe_id):
    conn = connect_db()
    cur = conn.cursor()

    # Remove from meal_plans first to avoid foreign key constraint errors
    cur.execute("DELETE FROM meal_plans WHERE recipe_id = %s", (recipe_id,))
    
    # Remove the recipe
    cur.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))

    conn.commit()
    cur.close()
    conn.close()

# Main function to interact with the CLI
def main():
    create_tables()

    print("\nView all recipes before adding new ones:")
    view_recipes()

    print("\nView all meal plans before adding new ones:")
    view_meal_plans()

    print("\nAdd a new recipe:")
    name = input("Recipe name: ")
    cooking_time = int(input("Cooking time (in minutes): "))
    instructions = input("Instructions: ")
    recipe_id = add_recipe(name, cooking_time, instructions)
    print(f"Recipe added with ID: {recipe_id}")

    print("\nAdd a new ingredient:")
    ingredient_name = input("Ingredient name: ")
    quantity = float(input("Quantity: "))
    unit = input("Unit (e.g., cup, gram): ")
    add_ingredient(ingredient_name, quantity, unit)
    print("Ingredient added.")

    print("\nCreate a new meal plan:")
    date = input("Date (YYYY-MM-DD): ")
    meal_type = input("Meal type (e.g., breakfast, lunch, dinner): ")
    create_meal_plan(recipe_id, date, meal_type)
    print("Meal plan created.")

    print("\nView all recipes after additions:")
    view_recipes()

    print("\nView all meal plans after additions:")
    view_meal_plans()

    print("\nDelete a recipe:")
    recipe_id_to_delete = int(input("Enter the ID of the recipe to delete: "))
    delete_recipe(recipe_id_to_delete)
    print(f"Recipe with ID {recipe_id_to_delete} deleted.")

    print("\nView all recipes after deletion:")
    view_recipes()

    print("\nView all meal plans after deletion:")
    view_meal_plans()

if __name__ == "__main__":
    main()
