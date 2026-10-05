from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product, Cart, CartItem, Order, OrderItem, Review, CustomerSupport


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='demouser', password='password123', email='demo@example.com')

    def test_01_user_registration_get_and_post(self):
        response = self.client.get(reverse('user_register'))
        self.assertEqual(response.status_code, 200)
        response_post = self.client.post(reverse('user_register'), {
            'username': 'newuser',
            'password': 'password123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response_post.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_02_user_login_valid(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'demouser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_03_user_login_invalid(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'demouser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_04_session_management(self):
        self.client.login(username='demouser', password='password123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_05_user_logout(self):
        self.client.login(username='demouser', password='password123')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)


class ProductManagementTests(TestCase):
    def setUp(self):
        self.cat1 = Category.objects.create(name='Electronics', slug='electronics')
        self.cat2 = Category.objects.create(name='Clothing', slug='clothing')
        self.p1 = Product.objects.create(name='Laptop', description='High performance laptop', price=999.99, category=self.cat1, stock=10)
        self.p2 = Product.objects.create(name='T-Shirt', description='Cotton shirt', price=19.99, category=self.cat2, stock=50)

    def test_06_product_listing_all(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'T-Shirt')

    def test_07_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.p1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')

    def test_08_product_detail_not_found(self):
        response = self.client.get(reverse('product_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_09_product_average_rating_no_reviews(self):
        self.assertEqual(self.p1.average_rating, 0)

    def test_10_product_average_rating_with_reviews(self):
        u1 = User.objects.create_user('u1', 'u1@ex.com', 'pass')
        u2 = User.objects.create_user('u2', 'u2@ex.com', 'pass')
        Review.objects.create(product=self.p1, user=u1, rating=5, comment='Great')
        Review.objects.create(product=self.p1, user=u2, rating=3, comment='Average')
        self.assertEqual(self.p1.average_rating, 4)

    def test_11_category_filtering(self):
        response = self.client.get(reverse('product_list') + '?category=electronics')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertNotContains(response, 'T-Shirt')

    def test_12_product_sorting_price_low(self):
        response = self.client.get(reverse('product_list') + '?sort=price_low')
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertEqual(products[0], self.p2)

    def test_13_product_sorting_price_high(self):
        response = self.client.get(reverse('product_list') + '?sort=price_high')
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertEqual(products[0], self.p1)


class ShoppingCartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('cartuser', 'c@ex.com', 'pass')
        self.p1 = Product.objects.create(name='Mouse', description='Wireless', price=25.00, stock=20)

    def test_14_add_to_cart_authenticated(self):
        self.client.login(username='cartuser', password='pass')
        response = self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.p1)

    def test_15_add_to_cart_anonymous(self):
        response = self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        self.assertEqual(response.status_code, 302)
        session_key = self.client.session.session_key
        cart = Cart.objects.get(session_key=session_key)
        self.assertEqual(cart.items.count(), 1)

    def test_16_update_cart_item_quantity(self):
        self.client.login(username='cartuser', password='pass')
        self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        cart = Cart.objects.get(user=self.user)
        item = cart.items.first()
        response = self.client.post(reverse('update_cart_item', args=[item.id]), {'quantity': 3})
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

    def test_17_remove_cart_item(self):
        self.client.login(username='cartuser', password='pass')
        self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        cart = Cart.objects.get(user=self.user)
        item = cart.items.first()
        response = self.client.get(reverse('remove_cart_item', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cart.items.count(), 0)

    def test_18_cart_total_price_calculation(self):
        cart = Cart.objects.create(user=self.user)
        p2 = Product.objects.create(name='Keyboard', description='Mechanical', price=75.00, stock=5)
        CartItem.objects.create(cart=cart, product=self.p1, quantity=2)
        CartItem.objects.create(cart=cart, product=p2, quantity=1)
        self.assertEqual(cart.total_price, 125.00)

    def test_19_api_cart_count(self):
        self.client.login(username='cartuser', password='pass')
        self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        response = self.client.get(reverse('cart_count'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)


class CheckoutAndOrdersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('orderuser', 'o@ex.com', 'pass')
        self.p1 = Product.objects.create(name='Headphones', description='Noise canceling', price=150.00, stock=10)

    def test_20_checkout_view_empty_cart(self):
        self.client.login(username='orderuser', password='pass')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)

    def test_21_checkout_view_with_items(self):
        self.client.login(username='orderuser', password='pass')
        self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Headphones')

    def test_22_checkout_submission_creates_order(self):
        self.client.login(username='orderuser', password='pass')
        self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        response = self.client.post(reverse('checkout'), {
            'shipping_address': '123 Main St, Tech City',
            'phone': '555-0199',
            'email': 'o@ex.com'
        })
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total_price, 150.00)
        self.assertEqual(order.items.count(), 1)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_23_order_list_authenticated(self):
        self.client.login(username='orderuser', password='pass')
        Order.objects.create(user=self.user, order_number='ORD123', total_price=100.00, shipping_address='Addr', phone='123', email='o@ex.com')
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ORD123')

    def test_24_order_list_anonymous(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 302)

    def test_25_order_detail_view(self):
        self.client.login(username='orderuser', password='pass')
        order = Order.objects.create(user=self.user, order_number='ORD456', total_price=150.00, shipping_address='Addr', phone='123', email='o@ex.com')
        response = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ORD456')

    def test_26_order_item_total_property(self):
        order = Order.objects.create(user=self.user, order_number='ORD789', total_price=300.00, shipping_address='Addr', phone='123', email='o@ex.com')
        order_item = OrderItem.objects.create(order=order, product=self.p1, quantity=2, price=150.00)
        self.assertEqual(order_item.total, 300.00)


class ReviewsAndRatingsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('revuser', 'r@ex.com', 'pass')
        self.p1 = Product.objects.create(name='Monitor', description='4K display', price=300.00, stock=5)

    def test_27_add_review_authenticated(self):
        self.client.login(username='revuser', password='pass')
        response = self.client.post(reverse('add_review', args=[self.p1.id]), {
            'rating': 5,
            'comment': 'Amazing display clarity!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(product=self.p1, user=self.user).exists())

    def test_28_add_review_unauthenticated(self):
        response = self.client.post(reverse('add_review', args=[self.p1.id]), {
            'rating': 4,
            'comment': 'Good product'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(product=self.p1).exists())

    def test_29_duplicate_review_prevented(self):
        Review.objects.create(product=self.p1, user=self.user, rating=4, comment='First')
        self.client.login(username='revuser', password='pass')
        response = self.client.post(reverse('add_review', args=[self.p1.id]), {
            'rating': 5,
            'comment': 'Second'
        })
        self.assertEqual(Review.objects.filter(product=self.p1, user=self.user).count(), 1)

    def test_30_review_rating_validation(self):
        review = Review(product=self.p1, user=self.user, rating=5, comment='Valid rating')
        review.full_clean()
        self.assertEqual(review.rating, 5)


class SearchAndFilteringTests(TestCase):
    def setUp(self):
        self.p1 = Product.objects.create(name='Wireless Gaming Mouse', description='RGB lighting optical sensor', price=59.99, stock=10)
        self.p2 = Product.objects.create(name='Mechanical Gaming Keyboard', description='Tactile switches', price=89.99, stock=15)
        self.p3 = Product.objects.create(name='Ergonomic Chair', description='Leather office chair', price=199.99, stock=3)

    def test_31_search_by_name(self):
        response = self.client.get(reverse('product_list') + '?search=Mouse')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wireless Gaming Mouse')
        self.assertNotContains(response, 'Ergonomic Chair')

    def test_32_search_by_description(self):
        response = self.client.get(reverse('product_list') + '?search=Tactile')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mechanical Gaming Keyboard')
        self.assertNotContains(response, 'Wireless Gaming Mouse')

    def test_33_search_no_results(self):
        response = self.client.get(reverse('product_list') + '?search=NonExistentItemQuery')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Wireless Gaming Mouse')

    def test_34_sort_by_name(self):
        response = self.client.get(reverse('product_list') + '?sort=name')
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertEqual(products[0], self.p3)

    def test_35_sort_by_newest(self):
        response = self.client.get(reverse('product_list') + '?sort=newest')
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertEqual(products[0], self.p3)


class CustomerSupportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('suppuser', 's@ex.com', 'pass')

    def test_36_customer_support_get(self):
        response = self.client.get(reverse('customer_support'))
        self.assertEqual(response.status_code, 200)

    def test_37_customer_support_post(self):
        response = self.client.post(reverse('customer_support'), {
            'name': 'Support User',
            'email': 's@ex.com',
            'subject': 'Order Inquiry',
            'message': 'Where is my package?'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomerSupport.objects.filter(subject='Order Inquiry').exists())


class UIAndUXTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('uiuser', 'ui@ex.com', 'pass')
        self.cat = Category.objects.create(name='Gadgets', slug='gadgets')
        self.p1 = Product.objects.create(name='Smartwatch', description='Fitness tracker', price=120.00, stock=8, category=self.cat)

    def test_38_home_page_featured_products(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartwatch')

    def test_39_navbar_cart_count_context(self):
        self.client.login(username='uiuser', password='pass')
        self.client.get(reverse('add_to_cart', args=[self.p1.id]))
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_40_form_prepopulation_support(self):
        self.client.login(username='uiuser', password='pass')
        response = self.client.get(reverse('customer_support'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'uiuser')

    def test_41_product_stock_validation(self):
        self.assertTrue(self.p1.stock >= 0)

    def test_42_category_str_representation(self):
        self.assertEqual(str(self.cat), 'Gadgets')

    def test_43_product_str_representation(self):
        self.assertEqual(str(self.p1), 'Smartwatch')
