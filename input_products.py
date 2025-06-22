import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'login_app/database.db')

def input_prod():
    try:
        name = input(str("What is the product name? "))
        description = input(str("What is the product description? "))
        price = float(input(str("What is the product price? $")))
        stock = int(input(str("What is the stock quantity? ")))
        category = input(str("What is the product category? "))

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
        existing_product = cursor.fetchone()
        if existing_product:
            print("Product already exists.")
            return
        else:
            print("Adding product to database.")
            cursor.execute('''INSERT INTO products (name, description, price, stock, category) VALUES (?, ?, ?, ?, ?)''', (name, description, price, stock, category.lower()))
            connection.commit()
            print("Product added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}", exc_info=True)
    except ValueError as ve:
        print(f"Value error: {ve}", exc_info=True)
    except TypeError as te:
        print(f"Type error: {te}", exc_info=True)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        if connection:
            connection.close()

def bulk_insert_products():
    products = [
        (1, "The OG", "Seiko 5 Sports SRPL33, automatic movement, robust stainless steel case, day-date display, and 100m water resistance.", 99.98, 0, "5_Sports"),
        (2, "The Traveller", "Seiko 5 Sports SSK023, automatic GMT, stainless steel, 24-hour bezel, and sporty design for travelers.", 98.55, 19, "5_Sports"),
        (3, "The Navigator", "Seiko Astron SSJ029J1, GPS Solar, titanium case, perpetual calendar, and world time function.", 50.00, 49, "astron"),
        (4, "The Bold", "Seiko 5 Sports SSK019J-8, automatic GMT, stainless steel, rotating bezel, and bold color accents.", 50.34, 12, "5_Sports"),
        (5, "The Racer", "Seiko Prospex SPB519, automatic chronograph, stainless steel, tachymeter, and 100m water resistance.", 1004.55, 101, "prospex"),
        (6, "The Tech Titan", "Seiko Astron SSH180J1, GPS Solar, dual time, titanium case, and advanced timekeeping technology.", 5000.00, 12, "astron")
    ]
    
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        # Delete existing products if any
        cursor.execute("DELETE FROM products")
        
        # Insert new products
        cursor.executemany('''
            INSERT INTO products (id, name, description, price, stock, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', products)
        
        connection.commit()
        print("Products added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    # input_prod()
    bulk_insert_products()
