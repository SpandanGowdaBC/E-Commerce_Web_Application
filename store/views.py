from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
import random
import string
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review, CustomerSupport


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
    return cart


def home(request):
    """Home page with featured products"""
    products = Product.objects.all()[:8]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })


def product_list(request):
    """Product listing page with filters and sorting"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Sort
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/product_list.html', {
        'products': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort_by,
        'search_query': search_query,
    })


def product_detail(request, product_id):
    """Product detail page with reviews"""
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Check if user has already reviewed
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'user_review': user_review,
    })


def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.stock:
            return JsonResponse({'success': False, 'message': 'Insufficient stock'})
        
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': cart.items.count()
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def cart_view(request):
    """Shopping cart page"""
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Verify cart ownership
        cart = get_or_create_cart(request)
        if cart_item.cart != cart:
            return JsonResponse({'success': False, 'message': 'Unauthorized'})
        
        if quantity <= 0:
            cart_item.delete()
        else:
            if quantity > cart_item.product.stock:
                quantity = cart_item.product.stock
            cart_item.quantity = quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'item_total': float(cart_item.total_price),
            'cart_total': float(cart.total_price),
            'cart_count': cart.items.count()
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def remove_cart_item(request, item_id):
    """Remove item from cart"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = get_or_create_cart(request)
        
        if cart_item.cart != cart:
            return JsonResponse({'success': False, 'message': 'Unauthorized'})
        
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'cart_total': float(cart.total_price),
            'cart_count': cart.items.count()
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    if cart.items.count() == 0:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart')
    
    if request.method == 'POST':
        # Create order
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=order_number,
            total_price=cart.total_price,
            shipping_address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            # Update stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f'Order placed successfully! Order number: {order_number}')
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'store/checkout.html', {'cart': cart})


@login_required
def order_list(request):
    """User's order list"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    """Order detail page with tracking"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check authorization
    if request.user.is_authenticated and order.user != request.user:
        messages.error(request, 'You do not have permission to view this order')
        return redirect('home')
    
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def add_review(request, product_id):
    """Add or update product review"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '')
        
        review, created = Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        messages.success(request, 'Review submitted successfully!')
        return redirect('product_detail', product_id=product_id)
    
    return redirect('product_detail', product_id=product_id)


def customer_support(request):
    """Customer support page"""
    if request.method == 'POST':
        support = CustomerSupport.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, 'Your support request has been submitted. We will get back to you soon!')
        return redirect('customer_support')
    
    return render(request, 'store/customer_support.html')


def get_cart_count(request):
    """API endpoint to get cart count"""
    cart = get_or_create_cart(request)
    return JsonResponse({'count': cart.items.count()})


def user_login(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'store/login.html')


def user_register(request):
    """User registration page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'store/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'store/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('user_login')
    
    return render(request, 'store/register.html')


@login_required
def user_logout(request):
    """User logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
