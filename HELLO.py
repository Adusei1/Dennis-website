from flask import Flask, render_template_string, redirect, url_for, session, request

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management. This is crucial for security.
app.secret_key = 'your-super-secret-key-here'

# Mock product data. In a real application, this would come from a database.
products = [
    {'id': 1, 'name': "Men's Classic Shirt", 'description': "A comfortable and stylish shirt for all occasions.", 'price': 35.99, 'image': "https://placehold.co/400x400/808080/FFFFFF?text=Men's+Shirt", 'category': "men's clothes"},
    {'id': 2, 'name': "Women's Summer Dress", 'description': "A light and breezy dress perfect for summer.", 'price': 49.99, 'image': "https://placehold.co/400x400/FFC0CB/FFFFFF?text=Women's+Dress", 'category': "women's clothes"},
    {'id': 3, 'name': "Hydrating Facial Serum", 'description': "Keep your skin smooth and hydrated all day long.", 'price': 25.00, 'image': "https://placehold.co/400x400/87CEEB/FFFFFF?text=Facial+Serum", 'category': "cosmetics"},
    {'id': 4, 'name': "Men's Jeans", 'description': "Durable and fashionable jeans for everyday wear.", 'price': 55.00, 'image': "https://placehold.co/400x400/4169E1/FFFFFF?text=Men's+Jeans", 'category': "men's clothes"},
    {'id': 5, 'name': "Women's Blouse", 'description': "An elegant blouse for a sophisticated look.", 'price': 30.50, 'image': "https://placehold.co/400x400/FFC0CB/FFFFFF?text=Women's+Blouse", 'category': "women's clothes"},
    {'id': 6, 'name': "Lipstick Set", 'description': "A vibrant set of long-lasting lipsticks.", 'price': 45.00, 'image': "https://placehold.co/400x400/FF69B4/FFFFFF?text=Lipstick+Set", 'category': "cosmetics"},
]

# A dictionary to store products by their ID for easy lookup.
product_dict = {p['id']: p for p in products}

# HTML templates for the application
# We'll put all the HTML and CSS in here for a self-contained solution.
base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My E-Commerce Store</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7fafc;
            color: #2d3748;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: auto;
            padding: 1.5rem;
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background-color: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: #4c51bf;
            text-decoration: none;
        }
        .nav-links a {
            margin-left: 1.5rem;
            color: #4a5568;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        .nav-links a:hover {
            color: #4c51bf;
        }
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }
        .product-card {
            background-color: white;
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        .product-card:hover {
            transform: translateY(-5px);
        }
        .product-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid #e2e8f0;
        }
        .product-card-content {
            padding: 1rem;
        }
        .product-card h3 {
            font-size: 1.25rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }
        .product-card p {
            font-size: 0.875rem;
            color: #718096;
            margin-bottom: 1rem;
        }
        .product-card .price {
            font-size: 1.5rem;
            font-weight: bold;
            color: #4c51bf;
            display: block;
            margin-bottom: 1rem;
        }
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: #4c51bf;
            color: white;
            text-align: center;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            transition: background-color 0.3s ease;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        .btn-secondary {
            background-color: #e2e8f0;
            color: #2d3748;
        }
        .btn:hover {
            background-color: #3f479a;
        }
        .btn-secondary:hover {
            background-color: #cbd5e0;
        }
        .cart-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1.5rem;
            background-color: white;
            border-radius: 0.75rem;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .cart-table th, .cart-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        .cart-table th {
            background-color: #f7fafc;
            font-weight: 600;
        }
        .cart-total {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 1.5rem;
        }
        .cart-total span {
            color: #4c51bf;
            margin-left: 0.5rem;
        }
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                align-items: flex-start;
                padding-bottom: 1rem;
            }
            .nav-links {
                margin-top: 1rem;
            }
            .nav-links a {
                margin-left: 0;
                margin-right: 1rem;
            }
            .products-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="{{ url_for('index') }}" class="logo">My E-Commerce</a>
        <div class="nav-links">
            <a href="{{ url_for('products_page') }}">Products</a>
            <a href="{{ url_for('cart_page') }}">Cart ({{ session.get('cart', {}) | length }})</a>
        </div>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# Home Page Template
home_template = base_html + """
{% block content %}
    <header style="text-align: center; padding: 4rem 0; background-color: white; border-radius: 0.75rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h1 style="font-size: 3rem; font-weight: bold; margin-bottom: 1rem; color: #1a202c;">Welcome to Our Store!</h1>
        <p style="font-size: 1.25rem; color: #4a5568;">Your one-stop shop for cosmetics and clothes.</p>
        <a href="{{ url_for('products_page') }}" class="btn" style="margin-top: 2rem; width: auto; padding: 1rem 2rem;">Shop Now</a>
    </header>
{% endblock %}
"""

# Products Page Template
products_template = base_html + """
{% block content %}
    <h1 style="font-size: 2rem; font-weight: bold; margin-bottom: 1.5rem;">All Products</h1>
    <div class="products-grid">
        {% for product in products %}
        <div class="product-card">
            <img src="{{ product.image }}" alt="{{ product.name }}">
            <div class="product-card-content">
                <h3>{{ product.name }}</h3>
                <p>{{ product.description }}</p>
                <span class="price">${{ "%.2f"|format(product.price) }}</span>
                <a href="{{ url_for('add_to_cart', product_id=product.id) }}" class="btn">Add to Cart</a>
            </div>
        </div>
        {% endfor %}
    </div>
{% endblock %}
"""

# Cart Page Template
cart_template = base_html + """
{% block content %}
    <h1 style="font-size: 2rem; font-weight: bold; margin-bottom: 1.5rem;">Shopping Cart</h1>
    {% if not cart %}
        <p style="color: #718096;">Your cart is empty.</p>
    {% else %}
        <table class="cart-table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                {% for item in cart %}
                <tr>
                    <td>{{ item.name }}</td>
                    <td>${{ "%.2f"|format(item.price) }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>${{ "%.2f"|format(item.price * item.quantity) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="cart-total">
            Total: <span>${{ "%.2f"|format(total) }}</span>
        </div>
        <div style="margin-top: 1.5rem; text-align: right;">
            <a href="{{ url_for('checkout') }}" class="btn" style="width: auto;">Proceed to Checkout</a>
        </div>
    {% endif %}
{% endblock %}
"""

# Checkout Confirmation Template
checkout_template = base_html + """
{% block content %}
    <div style="text-align: center; padding: 4rem 0; background-color: white; border-radius: 0.75rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h1 style="font-size: 3rem; font-weight: bold; color: #38a169;">Thank you!</h1>
        <p style="font-size: 1.25rem; color: #4a5568; margin-top: 1rem;">Your order has been placed successfully.</p>
        <a href="{{ url_for('products_page') }}" class="btn" style="margin-top: 2rem; width: auto; padding: 1rem 2rem;">Continue Shopping</a>
    </div>
{% endblock %}
"""

# The main route for the home page.
@app.route('/')
def index():
    return render_template_string(home_template)

# Route to display all products.
@app.route('/products')
def products_page():
    return render_template_string(products_template, products=products)

# Route to add a product to the cart.
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Get the current cart from the session, or an empty dictionary if it doesn't exist.
    cart = session.get('cart', {})
    product = product_dict.get(product_id)

    if product:
        # If the product is already in the cart, increment the quantity.
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        # Otherwise, add it to the cart with a quantity of 1.
        else:
            cart[str(product_id)] = {'name': product['name'], 'price': product['price'], 'quantity': 1}
        # Update the session with the new cart data.
        session['cart'] = cart
        return redirect(url_for('cart_page'))
    return redirect(url_for('products_page'))

# Route to view the shopping cart.
@app.route('/cart')
def cart_page():
    cart_data = session.get('cart', {})
    # Convert the dictionary of cart items to a list for easier iteration in the template.
    cart_items = [item for item in cart_data.values()]
    # Calculate the total price of all items in the cart.
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template_string(cart_template, cart=cart_items, total=total_price)

# Route to handle the checkout process.
@app.route('/checkout')
def checkout():
    # In a real app, this is where you'd process payment, save the order, etc.
    # For this prototype, we'll just clear the cart and show a success message.
    session.pop('cart', None)
    return render_template_string(checkout_template)

# Main entry point to run the application.
if __name__ == '__main__':
    # Running in debug mode is useful for development as it provides
    # detailed error messages and reloads the server on code changes.
    app.run(debug=True)

