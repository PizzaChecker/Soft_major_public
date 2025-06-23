from flask import Flask, Blueprint, render_template, send_from_directory, flash, redirect, session, url_for, request, abort, jsonify
from db_manager import db_manager
from models import Order
from login_app.encrypt import decrypt_data
import logging

app_log = logging.getLogger(__name__)

# /cart route
def base_cart():
    try: # tested*
        if "cart" not in session:
            return render_template("cart.html", cart_items=None, total_price=None)
        cart = session.get("cart", {})
        cart_items = []
        total_price = 0.0
        try: # tested*
            with db_manager.get_db() as conn:
                cur = conn.cursor()
                for product_id, quantity in cart.items():
                    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
                    product = cur.fetchone()
                    if product:
                        item_total = product['price'] * quantity
                        total_price += item_total
                        cart_items.append({
                            "product": dict(product),
                            "price": product['price'],
                            "quantity": quantity,
                            "total": item_total,
                        })
        except Exception as e:
            app_log.error(f"Database error: {e}", exc_info=True)
            flash("An error occurred while loading your cart, please try again later", "error")
            return redirect(url_for("products"))
        return render_template("cart.html", cart_items=cart_items, total_price=total_price)
    except Exception as e:
        app_log.error(f"Unknown error displaying cart: {e}", exc_info=True)
        flash("An error occurred while trying to display your cart, please try again later", "error")
        return redirect(url_for("products"))

# /cart/add/<product_id> route
def cart_add(product_id):
    try: # tested*
        cart = session.get("cart", {}) # If not cart return empty dict
        product_id_str = str(product_id)
        # Get quantity from form data
        try: # tested
            quantity = int(request.form.get("quantity", 1))
            if quantity < 1:
                raise ValueError("Quantity must be at least 1")
        except ValueError:
            flash("Invalid quantity", "error")
            return redirect(url_for("product_detail", product_id=product_id))

        # Check stock before adding to cart
        try: # tested*
            if not exceds_stock(product_id_str, cart, quantity): # Check stock level
                return redirect(url_for("product_detail", product_id=product_id))
        except Exception as e:
            app_log.error(f"Error checking stock: {e}", exc_info=True)
            flash("An error occurred while adding product stock, stock was not added. Please try again later", "error")
            return redirect(url_for("product_detail", product_id=product_id))

        if product_id_str in cart:
            cart[product_id_str] += quantity  # Increase quantity
        else:
            cart[product_id_str] = quantity  # Add new item with quantity

        session["cart"] = cart
        app_log.info(f"Product {product_id} added to cart with quantity {quantity}.")
        flash(f"Added {quantity} item(s) to cart", "success")
        return redirect(url_for("product_detail", product_id=product_id))
    except Exception as e:
        app_log.error(f"Unknown error adding product to cart: {e}", exc_info=True)
        flash("An error occurred while adding product to cart, please try again later", "error")
        return redirect(url_for("product_detail", product_id=product_id))

# /cart/add route for AJAX requests
def ajax_cart_add():
    try: # tested*
        if not request.is_json:
            return jsonify(success=False, message="Invalid request format"), 400 # Check if request is JSON
        data = request.get_json() # Get JSON data from request
        product_id = str(data.get("product_id"))
        quantity = int(data.get("quantity", 1))
        cart = session.get("cart", {})
        try: # tested*
            if not exceds_stock(product_id, cart, quantity):
                return jsonify(success=False, message="Exceeds stock limit", quantity=0)
        except Exception as e:
            app_log.error(f"Error checking stock for AJAX add: {e}", exc_info=True)
            return jsonify(success=False, message="An error occurred while checking stock"), 500
        if quantity < 1: # Should not need to check this just backup
            return jsonify(success=False, message="Invalid quantity", quantity=0)
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        session["cart"] = cart
        return jsonify(success=True, message="Added to cart", quantity=cart[product_id])
    except Exception as e:
        app_log.error(f"Error adding product to cart via AJAX: {e}", exc_info=True)
        return jsonify(success=False, message="An error occurred while increasing product amount"), 500

# /cart/remove_one route for AJAX requests
def ajax_cart_remove():
    try: # tested*
        if not request.is_json: # Should not run into this, but just in case
            app_log.warning("Invalid request format for AJAX cart remove")
            return jsonify(success=False, message="Invalid request format"), 400
        data = request.get_json() # Get JSON data from request
        product_id = str(data.get("product_id"))
        cart = session.get("cart", {})
        if product_id in cart:
            if cart[product_id] > 1:
                cart[product_id] -= 1
                session["cart"] = cart
                return jsonify(success=True, message="Removed one from cart", quantity=cart[product_id]) # Return updated quantity
            else:
                del cart[product_id]
                session["cart"] = cart
                return jsonify(success=True, message="Removed item from cart", quantity=0)
        return jsonify(success=False, message="Product not in cart")
    except Exception as e:
        app_log.error(f"Error removing product from cart via AJAX: {e}", exc_info=True)
        return jsonify(success=False, message="An error occurred while removing product from cart"), 500

# /cart/delete route for AJAX requests delete all of product from cart
def ajax_cart_delete(): # clear cart
    try: # tested*
        if not request.is_json:  # Should not run into this, but just in case
            app_log.warning("Invalid request format for AJAX cart delete")
            return jsonify(success=False, message="Invalid request format"), 400
        data = request.get_json()
        product_id = str(data.get("product_id"))
        cart = session.get("cart", {})
        if product_id in cart:
            del cart[product_id]
            session["cart"] = cart
            return jsonify(success=True, message="Product removed from cart")
        return jsonify(success=False, message="Product not in cart")
    except Exception as e:
        app_log.error(f"Error deleting product from cart via AJAX: {e}", exc_info=True)
        return jsonify(success=False, message="An error occurred while deleting product from cart"), 500

# /cart/clear route, clears the cart
def clear_cart():
    try:
        session.pop("cart", None)
        flash("Cart has been cleared.", "success")
        app_log.info("Cart cleared for user.")
        return redirect(url_for("cart"))
    except Exception as e:
        app_log.error(f"Error clearing cart: {e}", exc_info=True)
        flash("An error occurred while clearing your cart. Please try again later.", "error")
        return redirect(url_for("cart"))


# Non-main processing routes

def get_cart_address_info(): # Don't need expection as this is handled in the checkout route, tested*
    user_id = session.get("user_id")
    if not user_id:
        raise Exception("User not found")
    with db_manager.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT address FROM users WHERE id = ?", (user_id,))
            user = cur.fetchone()
            if user:
                address = user['address']
                return decrypt_data(address)
            else:
                raise Exception("User not found")

def exceds_stock(product_id, cart, quantity):
    try: # tested*
        with db_manager.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
            product = cur.fetchone()
            if not product:
                flash("Product not found", "error")
                return redirect(url_for("products"))
            stock = product["stock"]
            current_in_cart = cart.get(product_id, 0)
            if quantity + current_in_cart > stock:
                flash(f"Cannot add {quantity} item(s). Already got {current_in_cart} in cart. Exceeds Max amount of stock, {stock}", "error")
                return False
            return True
    except Exception as e:
        app_log.error(f"Error checking stock for product {product_id}: {e}", exc_info=True)
        raise e