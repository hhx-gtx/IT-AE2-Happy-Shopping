from django.test import TestCase
from django.urls import reverse
from .models import User, Product, Category, Order, OrderItem
import json



class ShopTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass", name="Test User")
        category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.00,
            image="test.jpg",
            category=category
        )

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('home'))
        print("[Login Test] User login success test passed!")

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {'username': 'wrong', 'password': 'wrongpass'})
        self.assertContains(response, "Invalid username or password")
        print("[Login Test] User login failure test passed!")

    def test_home_page(self):
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        print("[Home Page Test] Home page product display test passed!")

    def test_add_to_cart(self):
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), {
            'variant_Color': 'Black',
            'quantity': 1
        })
        self.assertRedirects(response, reverse('cart'))
        cart = self.client.session['cart']
        self.assertEqual(len(cart), 1)
        print("[Cart Test] Add product to cart test passed!")

    def test_create_order(self):
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        cart = {
            f"{self.product.id}-Black-Large": {
                "product_id": self.product.id,
                "name": self.product.name,
                "price": float(self.product.price),
                "image": self.product.image,
                "quantity": 2,
                "variants": json.dumps({"Color": "Black", "Size": "Large"}),
            }
        }
        session = self.client.session
        session['cart'] = cart
        session.save()

        response = self.client.post(reverse('create_order'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        order = Order.objects.first()
        order_item = order.items.first()
        self.assertEqual(order_item.product_name, self.product.name)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, self.product.price)
        self.assertEqual(order_item.get_variants(), {"Color": "Black", "Size": "Large"})
        print("[Order Test] Create new order with items and variants test passed!")

    def test_list_orders(self):
        order = Order.objects.create(order_id="ORD123", total_price=200.00)
        OrderItem.objects.create(
            order=order,
            product_name=self.product.name,
            price=self.product.price,
            quantity=2,
            variants='{"Color": "Black", "Size": "Large"}'
        )
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ORD123")
        self.assertContains(response, "£200.00")
        print("[Order Test] List all orders for user test passed!")
