import os
import django

# Setting up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from shop.models import Product, Category, ProductVariant

# Define categories and product data
categories = ["Electronics", "Clothing", "Household"]
products = [
    {
        "name": "iPhone 15 pro max",
        "description": "Latest Apple iPhone with A17 chip and improved camera.",
        "price": 969.00,
        "image": "products/iphone15.jpg",
        "category": "Electronics",
        "variants": {
            "Color": ["Black", "Blue", "Silver"],
            "Storage": ["256GB", "512GB", "1T"]
        }
    },
    {
        "name": "Automatic umbrella",
        "description": "Windproof and waterproof automatic umbrella.",
        "price": 10.99,
        "image": "products/umbrella.jpg",
        "category": "Household",
        "variants": {
            "Color": ["Black", "Red"],
            "Size": ["Small", "Medium", "Large"]
        }
    },
    {
        "name": "Laundry Pods",
        "description": "Tide hygienic clean power pods.",
        "price": 15.99,
        "image": "products/tide_pods.jpg",
        "category": "Household",
        "variants": {
            "Color": ["Black", "Red"],
            "Size": ["Small", "Medium", "Large"]
        }  # No specifications
    },
    {
        "name": "Men's regular suits",
        "description": "High-quality men's formal suit.",
        "price": 160.00,
        "image": "products/suit.jpg",
        "category": "Clothing",
        "variants": {
            "Color": ["Black", "Navy Blue"],
            "Size": ["S", "M", "L", "XL"]
        }
    },
]

# Insert Category
category_objects = {}
for category_name in categories:
    category, created = Category.objects.get_or_create(name=category_name)
    category_objects[category_name] = category
    if created:
        print(f"Inserted category: {category_name}")
    else:
        print(f"Category already exists: {category_name}")

# Insert Product & Specifications
for product_data in products:
    category = category_objects[product_data["category"]]  # Get the classification object
    variants = product_data.pop("variants", {})  # Retrieve specification data
    product, created = Product.objects.get_or_create(
        name=product_data["name"],
        defaults={**product_data, "category": category}
    )

    if created:
        print(f"Inserted product: {product.name} ({category.name})")
    else:
        print(f"Product already exists: {product.name} ({category.name})")

    # Insert product specifications
    for variant_type, values in variants.items():
        for value in values:
            variant, variant_created = ProductVariant.objects.get_or_create(
                product=product, variant_type=variant_type, variant_value=value
            )
            if variant_created:
                print(f"    Added variant: {variant_type} = {value}")
            else:
                print(f"    Variant already exists: {variant_type} = {value}")

print("Data insertion completed!")
