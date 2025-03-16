from functools import wraps
from django.shortcuts import redirect

# Check login status, redirect to login page if not logged in
def session_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper



# Calculate total price for cart and direct purchase
def calculate_total_price(cart, direct_purchase=None):
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    if direct_purchase:
        total += direct_purchase["price"] * direct_purchase["quantity"]
    return total
