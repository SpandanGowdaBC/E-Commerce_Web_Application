# Local Store E-commerce Platform

A complete e-commerce website built with Django (Python) and SQLite for backend, and HTML, CSS, and JavaScript for frontend. This platform enables customers to browse and purchase products online with a full-featured shopping experience.

## Features

### Core Requirements ✅
- **Product Listings**: Browse products with images, descriptions, and prices
- **Shopping Cart**: Add, update, and remove items from cart
- **Product Details**: Detailed product pages with full information

### Optional Features ✅
- **Order Tracking**: Track order status with visual progress indicators
- **User Reviews**: Customers can rate and review products
- **Customer Support**: Contact form for customer inquiries
- **Sort & Filters**: Filter by category, search products, and sort by price/name/newest

## Technology Stack

- **Backend**: Django 4.2.7, SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Image Handling**: Pillow
- **Icons**: Font Awesome 6.4.0

## Project Structure

```
Local_Store_ecommerce/
├── localstore/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/               # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin configuration
│   └── templates/       # HTML templates
│       └── store/
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── media/               # User uploaded files (created after first run)
├── manage.py
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Migrations

Create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser (Admin Account)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin username, email, and password.

### Step 4: Create Media Directory

Create the media directory for product images:

```bash
mkdir media
```

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Admin Panel

1. Access the admin panel at `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. Add categories and products:
   - Go to "Categories" and add product categories
   - Go to "Products" and add products with images, descriptions, prices, and stock

### Customer Features

1. **Browse Products**: Visit the home page or products page to see all available products
2. **Search & Filter**: Use the search bar and filters on the products page
3. **View Product Details**: Click on any product to see full details and reviews
4. **Add to Cart**: Add products to your shopping cart
5. **Checkout**: Proceed to checkout and place orders
6. **Track Orders**: View order status and tracking information (if logged in)
7. **Write Reviews**: Rate and review products (requires login)
8. **Contact Support**: Submit support requests through the customer support page

### Shopping Cart

- Cart works for both logged-in users and anonymous users (session-based)
- Add items, update quantities, or remove items
- Cart persists across page visits

### Order Management

- Orders are automatically assigned unique order numbers
- Order statuses: Pending → Processing → Shipped → Delivered
- Visual tracking timeline shows order progress

## Database Models

- **Category**: Product categories
- **Product**: Products with name, description, price, image, stock
- **Cart**: Shopping cart (user or session-based)
- **CartItem**: Items in cart with quantities
- **Order**: Customer orders with shipping information
- **OrderItem**: Individual items in an order
- **Review**: Product reviews and ratings (1-5 stars)
- **CustomerSupport**: Support ticket system

## Customization

### Styling

Modify `static/css/style.css` to customize the appearance. The design uses CSS variables for easy color customization:

```css
:root {
    --primary-color: #4a90e2;
    --secondary-color: #7b68ee;
    --accent-color: #ff6b6b;
    /* ... */
}
```

### Adding Features

- Views are in `store/views.py`
- URLs are configured in `store/urls.py`
- Templates are in `store/templates/store/`
- Static files (CSS/JS) are in `static/`

## Production Deployment

Before deploying to production:

1. **Change SECRET_KEY**: Update `SECRET_KEY` in `localstore/settings.py`
2. **Set DEBUG = False**: Disable debug mode
3. **Configure ALLOWED_HOSTS**: Add your domain
4. **Use a production database**: Consider PostgreSQL instead of SQLite
5. **Set up static files**: Run `python manage.py collectstatic`
6. **Configure media files**: Set up proper media file serving
7. **Use environment variables**: Store sensitive data in environment variables

## Troubleshooting

### Images not displaying
- Ensure the `media` directory exists
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings.py
- Verify file permissions

### Cart not working
- Check browser cookies are enabled
- Verify session middleware is enabled in settings

### Admin panel not accessible
- Ensure you've created a superuser account
- Check that you're using the correct URL: `/admin/`

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, use the customer support feature in the application or contact the development team.

---

**Happy Shopping! 🛒**
