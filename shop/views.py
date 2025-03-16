from .models import Product, Category, ProductVariant, User, Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import random
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.contrib import messages
from .utils import session_login_required, calculate_total_price






# Handle user login and session management
def login_view(request):
    error_message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")


        try:
            user = User.objects.get(username=username, password=password)

            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('home')
        except User.DoesNotExist:
            error_message = "Invalid username or password. Please try again!"


    return render(request, "shop/login.html", {'error_message': error_message})



# Handle user logout and session clearing
def logout_view(request):
    request.session.flush()
    return redirect('login')






# Display home page with product listing and search/filter functionality
@session_login_required
def home(request):

    # if 'user_id' not in request.session:
    #     return redirect('login')
    user_name = request.session.get('user_name', 'Guest')

    query = request.GET.get("q", "")  # Get search keywords
    category_name = request.GET.get('category')
    # category_id = request.GET.get("category", "")  # Get the selected category ID

    categories = Category.objects.all()  # Get all categories
    products = Product.objects.all()  # Default query all products
    selected_category = None

    # Filter: By search keyword
    if query:
        products = products.filter(name__icontains=query)  # Fuzzy matching name

    # Filter: By Category
    # if category_id:
    #     products = products.filter(category_id=category_id)

    if category_name:
        try:
            selected_category = Category.objects.get(name__iexact=category_name)  # Exactly ignore case
            products = products.filter(category=selected_category)  # Filter by category
        except Category.DoesNotExist:
            products = Product.objects.none()  # The category does not exist, and an empty product list is returned.


    return render(request, "shop/home.html", {
        "categories": categories,
        "products": products,
        "query": query,
        "selected_category": selected_category,
        'user_name': user_name
    })





# Display product detail with variants
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = product.variants.all()  # Get all specifications of the current product
    variant_groups = {}  # Storage of different types of specifications

    for variant in variants:
        if variant.variant_type not in variant_groups:
            variant_groups[variant.variant_type] = []
        variant_groups[variant.variant_type].append(variant.variant_value)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'variant_groups': variant_groups
    })





# Display shopping cart content and total price
@session_login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    print("Current Cart:", cart)  # Ensure that the data in the session is correct

    cart_items = []
    total_price = 0

    for cart_key, item in cart.items():
        print("Processing cart_key:", cart_key)  # Print each cart_key to see if it is empty
        if not cart_key or '-' not in cart_key:  # Invalid cart_key is already being skipped here
            continue

        product_id = cart_key.split('-')[0]  # Get product ID
        product = get_object_or_404(Product, id=int(product_id))

        cart_items.append({
            'cart_key': cart_key,  # Make sure cart_key is passed
            'product': product,
            'quantity': item['quantity'],
            'selected_variants': item.get('variants', {}),
            'subtotal': product.price * item['quantity']
        })

        total_price += product.price * item['quantity']

    print("Final Cart Items:", cart_items)  # Observe whether cart_key is empty

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})






# Add product with variants and quantity to shopping cart
@session_login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    # Get the specification selected by the user
    selected_variants = {}
    for key, value in request.POST.items():
        if key.startswith("variant_"):
            selected_variants[key.replace("variant_", "")] = value

    # Get the quantity selected by the user
    try:
        quantity = int(request.POST.get("quantity", 1))  # Default is 1, ensure it is an integer
        if quantity <= 0:  # Prevent illegal quantities
            quantity = 1
    except ValueError:
        quantity = 1  # If the user passes illegal data, the default value is 1

    print("Selected Quantity:", quantity)  # Debug Information

    # Generate a unique cart_key (product ID + specification)
    variant_values = list(selected_variants.values())
    if variant_values:
        cart_key = f"{product_id}-" + "-".join(variant_values)
    else:
        cart_key = str(product_id)

    if not cart_key or cart_key.strip() == "":
        print("ERROR: Generated cart_key is empty!")
        return redirect("home")

    print("Generated cart_key:", cart_key)

    # Update Cart
    if cart_key in cart:
        cart[cart_key]["quantity"] += quantity  # Correctly add up the amount selected by the user
    else:
        cart[cart_key] = {
            "product_id": product.id,
            "name": product.name,
            "price": float(product.price),
            "image": product.image if product.image else "",
            "quantity": quantity,
            "variants": selected_variants,
        }

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")







# Update cart item quantity (increase or decrease)
@session_login_required
def update_cart(request, cart_key, action):
    cart = request.session.get('cart', {})

    if cart_key in cart:
        if action == 'increase':
            cart[cart_key]['quantity'] += 1
        elif action == 'decrease':
            cart[cart_key]['quantity'] -= 1
            if cart[cart_key]['quantity'] <= 0:
                del cart[cart_key]

    request.session['cart'] = cart
    return redirect('cart')





# Display purchase summary for checkout (cart and direct purchase)
@session_login_required
def purchase_view(request):
    cart = request.session.get('cart', {})
    direct_purchase = request.session.get('direct_purchase', None)

    # total_price = sum(item["price"] * item["quantity"] for item in cart.values())
    # if direct_purchase:  # If there are products that can be purchased immediately
    #     total_price += direct_purchase["price"] * direct_purchase["quantity"]

    total_price = calculate_total_price(cart, direct_purchase)

    shipping_fee = 5.00  # Set a flat shipping rate
    actual_payment = total_price + shipping_fee

    # Order Information
    purchase_info = {
        "user_name": "Jack",
        "address": "61 Ruthven Ln, Glasgow G12 9BG",
        "phone": "7879675534",
        "payment_method": "Visa **** 1234 ✅",
    }

    return render(request, "shop/purchase.html", {
        "cart_items": cart.values(),
        "direct_purchase": direct_purchase,  # Directly purchased products
        "total_price": total_price,
        "shipping_fee": shipping_fee,
        "actual_payment": actual_payment,
        "purchase_info": purchase_info,
    })





# Create order based on shopping cart and direct purchase items
@session_login_required
def create_order_view(request):
    cart = request.session.get('cart', {})  # Items in the shopping cart
    direct_purchase = request.session.get('direct_purchase', None)  # Items to buy now

    # If both the shopping cart and the buy now item are empty, jump back to the shopping cart
    if not cart and not direct_purchase:
        return redirect("cart")

    # Generate Order ID
    order_id = f"#{random.randint(100000000000, 999999999999)}"

    # # Calculate the total price
    # total_price = 0
    #
    # # Calculate the total price of items in the shopping cart
    # if cart:
    #     total_price += sum(item["price"] * item["quantity"] for item in cart.values())
    #
    # # Calculate the total price of a Buy It Now item
    # if direct_purchase:
    #     total_price += direct_purchase["price"] * direct_purchase["quantity"]


    total_price = calculate_total_price(cart, direct_purchase)


    shipping_fee = 5.00  # Set a flat shipping rate
    actual_payment = total_price + shipping_fee  # Calculate final payment amount

    # Create an order
    order = Order.objects.create(
        order_id=order_id,
        total_price=actual_payment,  # Deposit final payment amount (including postage)
    )

    # Stores the items in the shopping cart (if any)
    if cart:
        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                product_name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                variants=item.get("variants", {})
            )

    # Stores items for immediate purchase (if any)
    if direct_purchase:
        OrderItem.objects.create(
            order=order,
            product_name=direct_purchase["name"],
            price=direct_purchase["price"],
            quantity=direct_purchase["quantity"],
            variants=direct_purchase.get("variants", {})
        )

    # After the order is created:
    if direct_purchase:
        request.session["direct_purchase"] = None  # Clear only the "Buy Now" data
    if cart:
        request.session["cart"] = {}  # Empty the shopping cart after checkout

    request.session.modified = True

    # After the order is successfully created, jump to the order details page
    return redirect("order_detail", order_id=order.order_id)



# Display paginated order list
@session_login_required
def order_list_view(request):
    orders = Order.objects.all().order_by("-created_at")  # Sort by creation time in descending order

    # Show 5 orders per page
    paginator = Paginator(orders, 5)
    page_number = request.GET.get("page")  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the order data of the current page

    return render(request, "shop/orders.html", {"page_obj": page_obj})





# Delete selected orders
@session_login_required
def delete_orders_view(request):
    if request.method == "POST":
        order_ids = request.POST.getlist("order_ids")  # Get the order ID to be deleted
        if order_ids:
            Order.objects.filter(id__in=order_ids).delete()  # Deleting from the database
            messages.success(request, "Selected orders have been deleted.")
        else:
            messages.warning(request, "No orders selected for deletion.")

    return redirect("orders")





# Display detailed information of a specific order
@session_login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    return render(request, "shop/order_detail.html", {
        "order": order,
        "order_items": order.items.all(),  # Order Items
        "total_price": order.total_price,  # Ensure that the payment amount is displayed correctly on the front end
    })




# Handle direct purchase of a product with variants and quantity
@session_login_required
def direct_purchase_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get the specification selected by the user
    selected_variants = {}
    for key, value in request.POST.items():
        if key.startswith("variant_"):  # Get only specification-related data
            selected_variants[key.replace("variant_", "")] = value

    # Get quantity (default 1)
    quantity = int(request.POST.get("quantity", 1))

    # Stores information about products that can be purchased immediately
    request.session['direct_purchase'] = {
        "product_id": product.id,
        "name": product.name,
        "price": float(product.price),
        "image": product.image if product.image else "",
        "quantity": quantity,
        "variants": selected_variants,  # Deposit specification information
    }
    request.session.modified = True  # Marks the session as changed

    return redirect("purchase_direct")   # Go to payment page


