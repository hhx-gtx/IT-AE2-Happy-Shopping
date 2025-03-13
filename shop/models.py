from django.db import models
from django.utils import timezone
import json



class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name





class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255, blank=True)  # Storage image path
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.FloatField(default=4.5)  # Product Rating

    def __str__(self):
        return self.name




class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    variant_type = models.CharField(max_length=50)  # Specification type, such as 'Color', 'Size', 'Storage'
    variant_value = models.CharField(max_length=100)  # Specification value, for example 'Black', '512GB', 'Large'

    def __str__(self):
        return f"{self.product.name} - {self.variant_type}: {self.variant_value}"





class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True)  # Order Number
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Order amount
    created_at = models.DateTimeField(default=timezone.now)  # Creation time

    def __str__(self):
        return f"Order {self.order_id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    variants = models.TextField(default="{}")  # Saving JSON Strings

    def set_variants(self, variants_dict):
        """Store in JSON format"""
        self.variants = json.dumps(variants_dict)

    def get_variants(self):
        """Parsing JSON from a string"""
        return json.loads(self.variants)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
