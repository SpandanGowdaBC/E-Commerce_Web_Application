from django.core.management.base import BaseCommand
from store.models import Product, Category
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample products like Blinkit/Instamart'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories...')
        
        # Create categories
        fruits, _ = Category.objects.get_or_create(name='Fruits & Vegetables', slug='fruits-vegetables')
        dairy, _ = Category.objects.get_or_create(name='Dairy & Eggs', slug='dairy-eggs')
        beverages, _ = Category.objects.get_or_create(name='Beverages', slug='beverages')
        snacks, _ = Category.objects.get_or_create(name='Snacks & Munchies', slug='snacks')
        bakery, _ = Category.objects.get_or_create(name='Bakery & Breakfast', slug='bakery')
        personal_care, _ = Category.objects.get_or_create(name='Personal Care', slug='personal-care')
        household, _ = Category.objects.get_or_create(name='Household Essentials', slug='household')
        
        self.stdout.write('Creating products...')
        
        products_data = [
            # Fruits & Vegetables
            {'name': 'Fresh Bananas (1kg)', 'price': 45.00, 'category': fruits, 'stock': 50, 
             'description': 'Fresh, ripe bananas. Rich in potassium and natural sugars. Perfect for breakfast or snacks.'},
            {'name': 'Red Tomatoes (500g)', 'price': 35.00, 'category': fruits, 'stock': 40,
             'description': 'Fresh red tomatoes. Perfect for salads, curries, and cooking. Locally sourced.'},
            {'name': 'Onions (1kg)', 'price': 40.00, 'category': fruits, 'stock': 60,
             'description': 'Fresh onions. Essential ingredient for Indian cooking. Long shelf life.'},
            {'name': 'Potatoes (1kg)', 'price': 30.00, 'category': fruits, 'stock': 55,
             'description': 'Fresh potatoes. Versatile vegetable perfect for various dishes.'},
            {'name': 'Carrots (500g)', 'price': 50.00, 'category': fruits, 'stock': 35,
             'description': 'Fresh orange carrots. Rich in beta-carotene and vitamins.'},
            {'name': 'Green Capsicum (500g)', 'price': 60.00, 'category': fruits, 'stock': 30,
             'description': 'Fresh green bell peppers. Great for stir-fries and salads.'},
            
            # Dairy & Eggs
            {'name': 'Amul Full Cream Milk (1L)', 'price': 66.00, 'category': dairy, 'stock': 100,
             'description': 'Fresh full cream milk. Pasteurized and packed for freshness.'},
            {'name': 'Amul Butter (100g)', 'price': 55.00, 'category': dairy, 'stock': 80,
             'description': 'Pure butter. Made from fresh cream. Perfect for cooking and spreading.'},
            {'name': 'Farm Fresh Eggs (12 pcs)', 'price': 90.00, 'category': dairy, 'stock': 70,
             'description': 'Farm fresh eggs. Rich in protein. Grade A quality.'},
            {'name': 'Amul Cheese Slices (200g)', 'price': 120.00, 'category': dairy, 'stock': 50,
             'description': 'Processed cheese slices. Perfect for sandwiches and burgers.'},
            {'name': 'Curd (500g)', 'price': 45.00, 'category': dairy, 'stock': 60,
             'description': 'Fresh homemade style curd. Probiotic rich and creamy.'},
            {'name': 'Paneer (250g)', 'price': 85.00, 'category': dairy, 'stock': 45,
             'description': 'Fresh cottage cheese. Perfect for gravies and snacks.'},
            
            # Beverages
            {'name': 'Coca Cola (750ml)', 'price': 40.00, 'category': beverages, 'stock': 120,
             'description': 'Classic cola drink. Refreshing and carbonated.'},
            {'name': 'Pepsi (750ml)', 'price': 40.00, 'category': beverages, 'stock': 110,
             'description': 'Popular cola drink. Great taste and refreshment.'},
            {'name': 'Real Fruit Juice - Orange (1L)', 'price': 120.00, 'category': beverages, 'stock': 60,
             'description': '100% real fruit juice. No added preservatives. Rich in Vitamin C.'},
            {'name': 'Tata Tea Gold (500g)', 'price': 280.00, 'category': beverages, 'stock': 40,
             'description': 'Premium tea leaves. Rich aroma and strong flavor.'},
            {'name': 'Nescafe Classic Coffee (100g)', 'price': 220.00, 'category': beverages, 'stock': 50,
             'description': 'Instant coffee. Rich and aromatic. Perfect start to your day.'},
            {'name': 'Bisleri Water (1L Pack of 12)', 'price': 180.00, 'category': beverages, 'stock': 80,
             'description': 'Pure mineral water. Safe and refreshing. Pack of 12 bottles.'},
            
            # Snacks
            {'name': 'Lay\'s Classic Salted (70g)', 'price': 20.00, 'category': snacks, 'stock': 150,
             'description': 'Crispy potato chips. Classic salted flavor. Perfect snack.'},
            {'name': 'Kurkure Masala Munch (70g)', 'price': 20.00, 'category': snacks, 'stock': 140,
             'description': 'Crunchy corn snacks. Spicy masala flavor. Addictive taste.'},
            {'name': 'Parle-G Biscuits (500g)', 'price': 45.00, 'category': snacks, 'stock': 100,
             'description': 'Glucose biscuits. Classic taste loved by all ages.'},
            {'name': 'Oreo Cookies (137g)', 'price': 45.00, 'category': snacks, 'stock': 90,
             'description': 'Chocolate sandwich cookies. Creamy filling. Delicious treat.'},
            {'name': 'Haldiram Namkeen (200g)', 'price': 65.00, 'category': snacks, 'stock': 70,
             'description': 'Traditional namkeen mix. Spicy and crunchy.'},
            {'name': 'Britannia Good Day Cookies (200g)', 'price': 50.00, 'category': snacks, 'stock': 85,
             'description': 'Butter cookies. Rich and buttery taste.'},
            
            # Bakery
            {'name': 'Britannia Bread - White (400g)', 'price': 40.00, 'category': bakery, 'stock': 60,
             'description': 'Fresh white bread. Soft and fluffy. Perfect for sandwiches.'},
            {'name': 'Brown Bread (400g)', 'price': 45.00, 'category': bakery, 'stock': 55,
             'description': 'Whole wheat bread. Healthy and nutritious.'},
            {'name': 'Croissant (Pack of 2)', 'price': 80.00, 'category': bakery, 'stock': 40,
             'description': 'Buttery French croissants. Flaky and delicious.'},
            {'name': 'Muffins - Chocolate (Pack of 4)', 'price': 120.00, 'category': bakery, 'stock': 35,
             'description': 'Chocolate muffins. Moist and rich. Perfect for breakfast.'},
            
            # Personal Care
            {'name': 'Colgate Toothpaste (200g)', 'price': 95.00, 'category': personal_care, 'stock': 80,
             'description': 'Complete care toothpaste. Fights cavities and whitens teeth.'},
            {'name': 'Dove Soap (125g)', 'price': 65.00, 'category': personal_care, 'stock': 90,
             'description': 'Moisturizing soap. Gentle on skin. 1/4 moisturizing cream.'},
            {'name': 'Head & Shoulders Shampoo (340ml)', 'price': 280.00, 'category': personal_care, 'stock': 50,
             'description': 'Anti-dandruff shampoo. Clean and healthy hair.'},
            {'name': 'Lux Soap (125g)', 'price': 35.00, 'category': personal_care, 'stock': 100,
             'description': 'Beauty soap. Soft and smooth skin.'},
            
            # Household
            {'name': 'Surf Excel Detergent (1kg)', 'price': 120.00, 'category': household, 'stock': 70,
             'description': 'Powerful detergent. Removes tough stains. Suitable for all fabrics.'},
            {'name': 'Vim Dishwash Gel (750ml)', 'price': 95.00, 'category': household, 'stock': 65,
             'description': 'Effective dishwashing gel. Cuts through grease easily.'},
            {'name': 'Harpic Toilet Cleaner (1L)', 'price': 110.00, 'category': household, 'stock': 60,
             'description': 'Powerful toilet cleaner. Kills 99.9% germs. Fresh fragrance.'},
            {'name': 'Paper Napkins (Pack of 2)', 'price': 85.00, 'category': household, 'stock': 75,
             'description': 'Soft paper napkins. Absorbent and strong. Pack of 2.'},
        ]
        
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'price': Decimal(str(product_data['price'])),
                    'category': product_data['category'],
                    'stock': product_data['stock'],
                    'description': product_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} products!'))
        self.stdout.write('Note: Product images need to be added manually through admin panel.')
