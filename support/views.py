# support/views.py — XAVFSIZ VERSIYA (FAQAT SUPPORT STAFF + SUPERUSER)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Order, Product


# Support staff yoki superuser ekanligini tekshirish
def support_access_required(user):
    return user.is_superuser or user.groups.filter(name='Support Staff').exists()


@login_required
@user_passes_test(support_access_required, login_url='dashboard')  # agar ruxsat bo‘lmasa dashboardga yuboradi
def support_dashboard(request):
    orders = Order.objects.all().order_by('-purchased_at').select_related('product', 'user')

    context = {
        'orders': orders,
    }
    return render(request, 'support/dashboard.html', context)


@login_required
@user_passes_test(support_access_required, login_url='dashboard')
def support_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        # Status o‘zgartirish
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'shipping', 'delivered']:
            order.status = new_status

        # Yetkazib berish muddati
        new_days = request.POST.get('delivery_days')
        if new_days and new_days.isdigit():
            order.product.delivery_days = int(new_days)
            order.product.save(update_fields=['delivery_days'])

        order.save()
        messages.success(request, "Buyurtma holati va muddati yangilandi!")
        return redirect('support_order_detail', pk=pk)

    context = {
        'order': order,
    }
    return render(request, 'support/order_detail.html', context)