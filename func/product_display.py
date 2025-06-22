from flask import Flask, Blueprint, render_template, send_from_directory, flash, redirect, session, url_for, request, abort, jsonify
from db_manager import db_manager
from models import Order

import logging
app_log = logging.getLogger(__name__)

# /products route
def base_prod_display():# Fetch product details for all products
    try: # tested*
        product_list = []
        try: #tested*
            with db_manager.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM products")
                products = cur.fetchall()
                product_list = [dict(product) for product in products]
        except Exception as e:
            app_log.error(f"Database error: {e}", exc_info=True)
            flash("An error occurred while loading products, please try again later", "error")
            return redirect(url_for("index"))
        return render_template("products.html", products=product_list)
    except Exception as e:
        app_log.error(f"Error in base_prod_display: {e}", exc_info=True)
        flash("An unexpected error occurred, please try again later", "error")
        return redirect(url_for("index"))

# /product/<int:product_id> route
def prod_detail(product_id):# Fetch product details based on the product_id
    try: # tested*
        product = get_product_details(product_id)
        if product:
            return render_template("product_detail.html", product=product)
        else:
            flash("Product not found, an error may have occured, please try again later", "error")
            return redirect("/products")
    except Exception as e:
        app_log.error(f"Error in prod_detail: {e}", exc_info=True)
        flash("An error occurred while trying to retrieve product details, please try again later", "error")
        return redirect("/products")

# /category/<category_name> route
def category_display(category_name):# Fetch products for the given category
    try: # tested*
        product_list = []
        with db_manager.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE category = ?", (category_name,))
            products = cur.fetchall()
            product_list = [dict(product) for product in products]
        return render_template("category.html", category_name=category_name, products=product_list)
    except Exception as e:
        app_log.error(f"Database error: {e}", exc_info=True)
        flash("An error occurred while loading the category, please try again later", "error")
        return redirect(url_for("index"))

# used in prod detail
def get_product_details(product_id):
    try: # tested*
        with db_manager.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product = cur.fetchone()
            
            if product:
                return dict(product)  # Return all fields as a dictionary
        return None
    except Exception as e:
        app_log.error(f"Database error: {e}", exc_info=True)
        return None