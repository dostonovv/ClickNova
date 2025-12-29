# products/views.py — TO‘G‘RI VERSIYA (metod o‘chirildi)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from .models import Product, Category, Order

def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)

    if request.method == "POST":
        if product.stock <= 0:
            messages.error(request, "Mahsulot tugagan!")
            return redirect('product_detail', pk=pk)

        try:
            with db_transaction.atomic():
                product.stock -= 1
                product.save(update_fields=['stock'])

                # Chegirmali narxni hisoblab saqlaymiz
                final_price = product.get_discounted_price()

                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=1,
                    total_price=final_price
                )

            messages.success(request, "Sizning buyurtmangiz qabul qilindi! 24 soat ichida siz bilan bog‘lanamiz.")
            return redirect('product_list')

        except Exception as e:
            messages.error(request, "Xatolik yuz berdi. Qayta urinib ko‘ring.")
            return redirect('product_detail', pk=pk)

    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)
def discount_products(request):
    products = Product.objects.filter(is_active=True, discount_percent__gt=0).order_by('-discount_percent')
    context = {
        'products': products,
    }
    return render(request, 'products/discount_list.html', context)