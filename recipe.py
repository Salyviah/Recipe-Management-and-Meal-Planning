import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="recipe_management_meal_planning",
        user="wambui",
        password="wambui",
        host="localhost",
        port="5432"
    )

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

def main():
    create_tables()

    print("Add a new recipe:")
    name = input("Recipe name: ")
    cooking_time = int(input("Cooking time (in minutes): "))
    instructions = input("Instructions: ")
    recipe_id = add_recipe(name, cooking_time, instructions)
    print(f"Recipe added with ID: {recipe_id}")

    print("\nAdd a new ingredient:")
    ingredient_name = input("Ingredient name: ")
    quantity = float(input("Quantity: "))
    unit = input("Unit (e.g., cup, gram ): ")
    add_ingredient(ingredient_name, quantity, unit)
    print("Ingredient added.")

    print("\nCreate a new meal plan:")
    date = input("Date (YYYY-MM-DD): ")
    meal_type = input("Meal type (e.g., breakfast, lunch, dinner): ")
    create_meal_plan(recipe_id, date, meal_type)
    print("Meal plan created.")

if __name__ == "__main__":
    main()