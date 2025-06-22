from flask import Flask, Blueprint, render_template, send_from_directory, flash, redirect, session, url_for, request, abort, jsonify
from db_manager import db_manager
from models import Order, OrderItem
from datetime import datetime

import logging
app_log = logging.getLogger(__name__)


def order_his():
    try: # tested*
        if not session.get("Username_Login") or not session.get("user_id"):
            flash("You need to log in to view your order history", "warning")
            return redirect(url_for("main.login"))
        
        try: # tested*
            with db_manager.get_db() as conn:
                cur = conn.cursor()
                # Join orders, order_items and products to get all required information
                cur.execute("""
                    SELECT p.id, p.name, oi.quantity, oi.total_item_price, o.order_date, o.status, o.receipt_id, o.total_price
                    FROM orders o
                    JOIN order_items oi ON o.receipt_id = oi.receipt_id
                    JOIN products p ON oi.product_id = p.id
                    WHERE o.user_id = ?
                    ORDER BY o.order_date DESC, o.receipt_id
                """, (session["user_id"],))
                
                orders_list = []
                time_error = False
                for row in cur.fetchall():
                    # Parse the date string with microseconds
                    try:
                        order_date = datetime.strptime(row['order_date'], '%Y-%m-%d %H:%M:%S.%f')
                    except Exception as e:
                        time_error = True
                        app_log.error(f"Error parsing order date & time: {e}", exc_info=True)
                        order_date = datetime.strptime('2025-01-01 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
                    orders_list.append((
                        row['id'],  # product_id for image
                        row['name'],  # product name
                        row['quantity'],
                        row['total_item_price'],  # using item total price instead of order total
                        order_date,  # now a datetime object
                        row['status'],
                        row['receipt_id']
                    ))
                if time_error:
                    flash("An error occurred while trying to retrive a date(s) of an order, please try again later while we try to fix this issue. Time will appear as 01/01/2025 00:00", "error")
                return render_template("order_history.html", orders=orders_list)
                
        except Exception as e:
            app_log.error(f"Database error: {e}", exc_info=True)
            flash("An error occurred while fetching your order history, please try again later", "error")
            return redirect(url_for("main.user_dashboard"))
    except Exception as e:
        app_log.error(f"Error in order_his: {e}", exc_info=True)
        flash("An unexpected error occurred, please try again later", "error")
        return redirect(url_for("main.user_dashboard"))