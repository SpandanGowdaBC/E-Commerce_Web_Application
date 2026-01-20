# 🚀 Quick Start Guide

Get the Local Store E-commerce application running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- pip (Python package manager)
- Git (optional, for cloning)

## Installation Steps

### 1. Get the Code

**Option A: Clone with Git**
```bash
git clone https://github.com/yourusername/Local_Store_ecommerce.git
cd Local_Store_ecommerce
```

**Option B: Download ZIP**
- Download and extract the ZIP file
- Open terminal/command prompt in the extracted folder

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.7
- Pillow 10.1.0

### 3. Setup Database

```bash
python manage.py migrate
```

### 4. Create Admin Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin username and password.

### 5. Create Media Folder

```bash
mkdir media
```

### 6. Run the Server

```bash
python manage.py runserver
```

### 7. Access the Application

Open your browser and visit:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First Steps

### Add Products (via Admin Panel)

1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Click on **"Categories"** → **"Add Category"**
   - Name: Fruits & Vegetables
   - Slug: fruits-vegetables
   - Save
4. Click on **"Products"** → **"Add Product"**
   - Name: Fresh Bananas (1kg)
   - Description: Fresh, ripe bananas
   - Price: 45.00
   - Category: Fruits & Vegetables
   - Stock: 50
   - Upload an image (optional)
   - Save

### Test the Application

1. **Browse Products**: Go to http://127.0.0.1:8000/products/
2. **View Product**: Click on a product
3. **Add to Cart**: Click "Add to Cart"
4. **View Cart**: Click cart icon in navigation
5. **Checkout**: Click "Proceed to Checkout"
6. **Place Order**: Fill form and submit

## Common Commands

### Run Development Server
```bash
python manage.py runserver
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8080
```

### Database Issues
```bash
# Delete db.sqlite3 and start fresh
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading
```bash
# Make sure DEBUG=True in settings.py for development
```

## Next Steps

- 📖 Read the [full README](README.md)
- 🎯 Check out [FEATURES.md](FEATURES.md)
- 🧪 Review [TESTING_REPORT.md](TESTING_REPORT.md)
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Need Help?

- 📧 Email: champspand@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/Local_Store_ecommerce/issues)
- 📚 Documentation: See README.md

---

**Happy Coding! 🎉**
