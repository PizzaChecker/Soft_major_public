from flask import Flask, Blueprint, render_template, send_from_directory, flash, redirect, session, url_for, request, abort, jsonify
from db_manager import db_manager
from models import Order, OrderItem

import logging
import uuid
from datetime import datetime
import pytz

from func.cart import get_cart_address_info

app_log = logging.getLogger(__name__)

# /checkout route get and post handling
def checkout_func():
    try: # tested*
        cart = session.get("cart", {})
        if not cart:
            flash("Your cart is empty", "error")
            return redirect(url_for("products"))
        
        if not session.get("Username_Login"):
            flash("You need to log in to checkout", "warning")
            session["checkout_redirect"] = True
            return redirect(url_for("main.login"))
        
        if request.method == "POST":
            try: # tested*
                address = request.form.get("address")
                payment_method = request.form.get("payment_method")
            except Exception as e:
                app_log.error(f"Error getting form data: {e}", exc_info=True)
                flash("An error occurred while processing your order, nothing was executed. Please try again later", "error")
                return redirect(url_for("cart"))
            order_items = []
            total_price = 0.00


            try: # tested*
                # Verify products and calculate totals first
                with db_manager.get_db() as conn:
                    cur = conn.cursor()
                    
                    for product_id, quantity in cart.items():
                        product_id = int(product_id)
                        quantity = int(quantity)
                        
                        cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
                        product = cur.fetchone()
                        
                        if not product:
                            flash(f"Product not found: {product_id}", "error")
                            return redirect(url_for("cart"))
                        
                        if product['stock'] < quantity:
                            flash(f"Not enough stock for {product['name']}", "error")
                            return redirect(url_for("cart"))

                        item_total = product['price'] * quantity
                        total_price += item_total
                        
                        order_items.append({
                            'product_name': product['name'],
                            'quantity': quantity,
                            'price': product['price'],
                            'total': item_total,
                            'product_id': product_id
                        })

                # Now process the orders in a separate transaction
                with db_manager.get_session() as db_session:
                    # Update stock and create orders
                    with db_manager.get_db() as conn:
                        cur = conn.cursor()
                        receipt_id = str(uuid.uuid4()) # Generate a unique receipt ID
                        for item in order_items:
                            order_item = OrderItem(
                                receipt_id=receipt_id,
                                product_id=item['product_id'],
                                quantity=item['quantity'],
                                price=item['price'],
                                total_item_price=item['total']
                            )
                            db_session.add(order_item)
                        
                        # Get current time in AEST
                        aest = pytz.timezone('Australia/Sydney') # Used to get the current time in AEST
                        current_aest_time = datetime.now(aest)

                        # Create single order for all items
                        order = Order(
                            user_id=session["user_id"],
                            total_price=total_price,
                            order_date=current_aest_time,
                            status='pending',
                            receipt_id=receipt_id,
                            address=address
                        )
                        db_session.add(order)

                        # Update stock using raw SQL
                        for item in order_items: # Update stock for each item
                            cur.execute(
                                "UPDATE products SET stock = stock - ? WHERE id = ?",
                                (item['quantity'], item['product_id'])
                            )
                        
                        # Commit SQLite changes
                        conn.commit()

                        # Flush ORM changes
                        db_session.flush()

                # Clear cart and render receipt
                session.pop("cart", None)
                current_date = datetime.now()
                return render_template('receipt.html',
                                    order_date=current_date,
                                    user_address=address,
                                    items=order_items,
                                    total_price=total_price,
                                    payment_method=payment_method,
                                    receipt_id=receipt_id)

            except Exception as e:
                app_log.error(f"Error in checkout: {e}", exc_info=True)
                flash("An error occurred while processing your order, nothing was executed. Please try again later", "error")
                return redirect(url_for("cart"))


        # GET request handling
        try: # tested*
            cart_items = []
            total_price = 0.0
            
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
            address = get_cart_address_info()
            return render_template("checkout.html", cart_items=cart_items, total_price=total_price, address=address)
            
        except Exception as e:
            app_log.error(f"Error loading cart: {e}", exc_info=True)
            flash("An error occurred while loading your cart, please try again later", "error")
            return redirect(url_for("products"))
    except Exception as e:
        app_log.error(f"Error in checkout function: {e}", exc_info=True)
        flash("An unexpected error occurred, please try again later", "error")
        return redirect(url_for("products"))