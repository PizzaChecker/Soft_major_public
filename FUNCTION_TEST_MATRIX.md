# Function Test Matrix for Project

| Tested | Function Name         | File Location         | Description                                      | Notes |
|--------|----------------------|----------------------|--------------------------------------------------|-------|
| <input type="checkbox" checked>  | create_app           | main.py              | Initializes Flask app and configures extensions  |       |
| <input type="checkbox" checked>  | before_request       | main.py              | Runs before every request, checks session/params | Logs access |
| <input type="checkbox" checked>  | set_security_headers | main.py              | Sets security headers after each request         | Check Styling latter erorr? |
| <input type="checkbox" checked>  | index                | main.py              | Renders home page, fetches best sellers          | Logs error |
| <input type="checkbox" checked>  | init_db              | init_db.py           | Initializes the SQLite database with schema      | Prints errors |
| <input type="checkbox" checked>  | input_prod           | input_products.py    | Adds a product to the database from user input   | Prints errors |
| <input type="checkbox" checked>  | __ init __           | db_manager.py        | Initializes DatabaseManager                      |       |
| <input type="checkbox" checked>  | get_db               | db_manager.py        | Yields a SQLite DB connection                    |       |
| <input type="checkbox" checked>  | get_session          | db_manager.py        | Yields a SQLAlchemy session                      |       |
| <input type="checkbox" checked>  | __ del __            | db_manager.py        | Disposes SQLAlchemy engine                       |       |
| <input type="checkbox" checked>  | Order (class)        | models.py            | Represents an order in the database              |       |
| <input type="checkbox" checked>  | base_cart            | func/cart.py         | Renders cart page with items and total           |       |
| <input type="checkbox" checked>  | cart_add             | func/cart.py         | Adds product to cart from form                   |       |
| <input type="checkbox" checked>  | ajax_cart_add        | func/cart.py         | Adds product to cart via AJAX                    |       |
| <input type="checkbox" checked>  | ajax_cart_remove     | func/cart.py         | Removes one item from cart via AJAX              |       |
| <input type="checkbox" checked>  | ajax_cart_delete     | func/cart.py         | Deletes all of a product from cart via AJAX      |       |
| <input type="checkbox" checked>  | get_cart_address_info| func/cart.py         | Gets and decrypts user address from DB           |       |
| <input type="checkbox" checked>  | exceds_stock         | func/cart.py         | Checks if adding to cart exceeds stock           |       |
| <input type="checkbox" checked>  | checkout_func        | func/checkout.py     | Handles checkout GET and POST logic              |       |
| <input type="checkbox" checked>  | order_his            | func/order_history.py | Shows order history for logged-in user          |       |
| <input type="checkbox" checked>  | base_prod_display    | func/product_display.py | Renders all products page                     |       |
| <input type="checkbox" checked>  | prod_detail          | func/product_display.py | Renders product detail page                   |       |
| <input type="checkbox" checked>  | category_display     | func/product_display.py | Renders category page                         |       |
| <input type="checkbox" checked>  | get_product_details  | func/product_display.py | Fetches product details from DB               |       |

- Tested: Tick when tested (use <input type="checkbox"> for unticked, <input type="checkbox" checked> for tested)
- File Location: Where the function is found
- Description: Brief description of the function
- Notes: Additional context or comments
