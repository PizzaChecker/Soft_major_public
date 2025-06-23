from flask import Flask, Blueprint, render_template, send_from_directory, flash, redirect, session, url_for, request, abort, jsonify
import os
import logging
from flask_csp.csp import csp_header
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.errors import RateLimitExceeded

from login_app.rate_limit import init_limiter, handle_rate_limit_error
from login_app.login_main import login_main_blue, redirect_directions, check_session_timeout
from login_app.url_validation import is_safe_url

from func.checkout import checkout_func
from func.cart import base_cart, cart_add, ajax_cart_add, ajax_cart_remove, ajax_cart_delete, clear_cart
from func.order_history import order_his
from func.product_display import base_prod_display, prod_detail, category_display

from jinja2 import ChoiceLoader, FileSystemLoader
from db_manager import db_manager
import sys
from flask import jsonify

# https://github.com/hmisonne/E-commerce-Web-App/blob/master/unwrap/__init__.py # To look at latter

# Logging configuration
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

app = Flask(__name__)

# Configure template loader to look in both locations
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('login_app/templates'),
    FileSystemLoader('templates')
])

# Configure static files
app.static_folder = 'login_app/static'
# app.static_url_path = '/static'

# Static file handler for the second static folder
@app.route('/extra_static/<path:filename>')
def extra_static(filename):
    return send_from_directory('static', filename)

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'login_app/database.db')

def create_app(): # Does not need expection as handled in startup, tested*
    global app

    # Configuration
    secret_key_ = os.environ.get("VSCODE_SK_")
    app.secret_key = secret_key_
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Strict',
        SESSION_COOKIE_NAME='_secure_session',
        SESSION_COOKIE_PATH='/',
        SESSION_COOKIE_DOMAIN=None
    )

    # Initialise extensions
    csrf = CSRFProtect(app)
    limiter = init_limiter(app)
    
    # Register blueprints
    app.register_blueprint(login_main_blue)

    return app

@app.before_request # This function runs before every request, 
def before_request():
    try:
        # Check session timeout before each request.
        if check_session_timeout():
            return redirect_directions() # Redirects to slected page if session expired
        for key, value in request.args.items(): # Check all GET parameters
            if 'redirect' in key.lower() or 'url' in key.lower() or 'next' in key.lower(): # Check for potential redirect parameters
                if not is_safe_url(value): # Check if the URL is safe
                    app_log.warning(f"Blocked potentially malicious redirect: {value}")
                    abort(400) # Bad request if URL is not safe
        
        app_log.info(f"Accessing {request.endpoint} by {request.remote_addr}") # Log the request
    except Exception as e:
        app_log.critical(f"Error during before_request: {e}", exc_info=True)
        abort(500)

@app.after_request
def set_security_headers(response):
    try:
        try:
            response.headers['X-Content-Type-Options'] = 'nosniff' # Prevents MIME type sniffing
        except Exception as e:
            app_log.critical(f"Failed to set X-Content-Type-Options: {e}", exc_info=True)
        try:
            response.headers['X-Frame-Options'] = 'DENY' # Prevents embedding in iframes
        except Exception as e:
            app_log.critical(f"Failed to set X-Content-Type-Options: {e}", exc_info=True)
        try:
            response.headers['X-XSS-Protection'] = '1; mode=block' # Enables XSS filter
        except Exception as e:
            app_log.critical(f"Failed to set X-XSS-Protection: {e}", exc_info=True)
    except Exception as e:
        app_log.critical(f"Error during after_request setting security headers: {e}", exc_info=True)
    return response


@app.route("/")
@csp_header(
    {
        "base-uri": "'self'", # Restrict base URI to self
        "default-src": "'self'", # Default source for all content
        "style-src": "'self' 'unsafe-inline' https://stackpath.bootstrapcdn.com https://cdn.jsdelivr.net", # Allow Bootstrap CSS and other external styles
        "script-src": "'self' https://stackpath.bootstrapcdn.com https://cdn.jsdelivr.net",  # Allow Bootstrap JS and other external scripts
        "img-src": "'self' data:",  # Allow images from self, data URIs
        "media-src": "'self'", # Allow media from self
        "font-src": "'self'", # Allow fonts from self
        "object-src": "'self'", # Allow objects from self
        "child-src": "'self'", # Allow child resources from self
        "connect-src": "'self'", # Allow connections from self
        "worker-src": "'self'", # Allow web workers from self
        "report-uri": "/csp_report", # URL to report violations
        "frame-ancestors": "'none'", # Prevents the page from being embedded in iframes
        "form-action": "'self'", # Restrict form submissions to self
        "frame-src": "'none'", # Prevent embedding in iframes
    }
)
def index():
    best_sellers = [1,3,4,5]
    try: # tested*
        with db_manager.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id IN (?, ?, ?, ?)", best_sellers)
            products = cur.fetchall()
            best_sellers = [dict(product) for product in products]
            return render_template("home.html", products=best_sellers)
    except Exception as e:
        app_log.error(f"Database error: {e}", exc_info=True)
        flash("An error occurred while loading home page", "error")
        return render_template("home.html")

@app.route("/products")
def products():
    return base_prod_display()

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    return prod_detail(product_id)

@app.route("/category/<category_name>")
def category(category_name):
    return category_display(category_name)

@app.route("/cart")
def cart():
    return base_cart()

@app.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    return cart_add(product_id)

# AJAX: Add one item to cart
@app.route("/cart/add", methods=["POST"])
def cart_add_ajax():
    return ajax_cart_add()

# AJAX: Remove one item from cart
@app.route("/cart/remove_one", methods=["POST"])
def cart_remove_one_ajax():
    return ajax_cart_remove()

# AJAX: Delete all of a singular product from cart
@app.route("/cart/delete", methods=["POST"])
def cart_delete_ajax():
    return ajax_cart_delete()

# AJAX: Clear the entire cart
@app.route("/cart/clear", methods=["POST"])
def cart_clear():
    return clear_cart()

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    return checkout_func()

@app.route("/order_history")
def order_history():
    return order_his()

@app.template_filter('format_category')
def format_category(name):
    return name.replace('_', ' ').title()

# Error handling routes
@app.errorhandler(400) # Bad Request
def bad_request(error):
    app_log.warning(f"Bad request: {request.path} by {request.remote_addr}")
    return render_template("400.html", error="Bad Request - Invalid URL or parameters"), 400

@app.errorhandler(401) # Unauthorised
def Unauthorised(error):
    app_log.warning(f"Unauthorised access attempt to {request.path} by {request.remote_addr}")
    return render_template("401.html", error="Unauthorised access"), 401

@app.errorhandler(403) # Forbidden
def forbidden_access(error):
    app_log.warning(f"Forbidden access attempt to {request.path} by {request.remote_addr}")
    return render_template("401.html", error="Access is forbidden"), 403

@app.errorhandler(404) # Not Found
def page_not_found(e):
    app_log.error(f"Page not found: {request.path} by {request.remote_addr}")
    return render_template('404.html'), 404

@app.errorhandler(405) # Method Not Allowed
def method_not_allowed(error):
    app_log.error(f"Method not allowed: {request.method} on {request.path} by {request.remote_addr}")
    return render_template('405.html', error="Method not allowed"), 405

@app.errorhandler(413) # Payload Too Large
def content_too_large(error):
    app_log.warning(f"File size too large: {error}")
    return render_template("passerror.html", error="File is too large. Maximum size is 5 MB."), 413

@app.errorhandler(429) # Too Many Requests
@app.errorhandler(RateLimitExceeded) # Flask Specfic Limiter Error
def rate_limit_handler(e):
    app_log.warning(f"Rate limit exceeded: {e.description} on {request.path} by {request.remote_addr}")
    return handle_rate_limit_error(e)

@app.errorhandler(500) # Internal Server Error
def internal_server_error(e):
    app_log.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

@app.errorhandler(Exception) # Unhandled Exception
def handle_exception(e):
    app_log.critical(f"Unhandled exception: {e}", exc_info=True)
    return render_template("418.html"), 418

if __name__ == "__main__":
    try: # tested*
        app = create_app()
        app_log.info("Starting Flask app...")
        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:
        print("Critical error! Failed to start Flask App!")
        app_log.critical(f"Failed to start Flask app: {e}", exc_info=True)
        sys.exit(1)  # Exit with error code 1 if app fails to start