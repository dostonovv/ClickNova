# core/views.py — FINAL VERSIYA (SARFLAGAN PUL TO‘G‘RI + GALLERY UCHUN)
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from products.models import Product, Order


def register(request):
    if request.method == "POST":
        username = request.POST['username'].lstrip('@').strip()
        full_name = request.POST['full_name'].strip()
        phone = request.POST['phone_number'].strip()
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Parollar mos emas!")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu username band!")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro‘yxatdan o‘tgan!")
            return redirect('register')

        if CustomUser.objects.filter(phone_number=phone).exists():
            messages.error(request, "Bu telefon raqami allaqachon ro‘yxatdan o‘tgan!")
            return redirect('register')

        user = CustomUser.objects.create_user(
            username=username,
            full_name=full_name,
            phone_number=phone,
            email=email,
            password=password,
            is_active=True
        )

        login(request, user)
        messages.success(request, f"Xush kelibsiz, @{username}!")
        return redirect('dashboard')

    return render(request, 'core/register.html')


@login_required
def dashboard(request):
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]  # 8 ta ko‘proq ko‘rsatamiz
    context = {
        'latest_products': latest_products,
    }
    return render(request, 'core/dashboard.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST['username'].lstrip('@').strip()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username yoki parol noto‘g‘ri!")
    return render(request, 'core/login.html')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-purchased_at')
    total_spent_raw = orders.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
    total_spent = f"${float(total_spent_raw):.2f}"  # <--- to‘g‘ri format: $5.70
    total_orders = orders.count()

    context = {
        'orders': orders,
        'total_spent': total_spent,
        'total_orders': total_orders,
    }
    return render(request, 'core/profile.html', context)