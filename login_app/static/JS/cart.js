// Cart functionality has been moved to inline JavaScript in cart.html template
function initializeCart(csrfToken) {
    document.addEventListener('DOMContentLoaded', function() {
        // Add one to cart
        document.querySelectorAll('.btn-plus').forEach(btn => {
            btn.addEventListener('click', function() {
                const productId = this.dataset.productId;
                fetch('/cart/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
                    body: JSON.stringify({product_id: productId, quantity: 1})
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    location.reload();
                })
                .catch(error => {
                    alert('Failed to add item to cart, please try again.');
                    console.error(error);
                });
            });
        });

        // Remove one from cart
        document.querySelectorAll('.btn-minus').forEach(btn => {
            btn.addEventListener('click', function() {
                const productId = this.dataset.productId;
                fetch('/cart/remove_one', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
                    body: JSON.stringify({product_id: productId})
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    location.reload();
                })
                .catch(error => {
                    alert('Failed to remove item from cart, please try again.');
                    console.error(error);
                });
            });
        });

        // Delete all of product from cart
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', function() {
                const productId = this.dataset.productId;
                fetch('/cart/delete', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
                    body: JSON.stringify({product_id: productId})
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    location.reload();
                })
                .catch(error => {
                    alert('Failed to delete item from cart, please try again.');
                    console.error(error);
                });
            });
        });
    });
}