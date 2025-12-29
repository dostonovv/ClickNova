# products/admin.py — KO‘P RASM (GALLERY) + CHEGIRMA BILAN FINAL VERSIYA
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, ProductImage  # <--- ProductImage qo‘shildi
from decimal import Decimal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # yangi mahsulot qo‘shganda 3 ta bo‘sh rasm joyi chiqadi
    fields = ('image', 'alt_text', 'is_main')
    verbose_name = "Rasm"
    verbose_name_plural = "Rasmlar"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'discount_percent', 'discounted_price_display', 'stock', 'is_active', 'created_at'
    )
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'discount_percent', 'stock', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'price', 'discount_percent', 'stock', 'is_active', 'delivery_days')
        }),
        ('Tavsif', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    inlines = [ProductImageInline]  # <--- KO‘P RASM QO‘SHISH UCHUN

    def discounted_price_display(self, obj):
        if obj.discount_percent > 0:
            discount_amount = obj.price * Decimal(str(obj.discount_percent)) / Decimal('100')
            discounted = obj.price - discount_amount
            original_str = f"${float(obj.price):.2f}"
            discounted_str = f"${float(discounted):.2f}"
            return format_html(
                '<strong style="color:green;">{}</strong> <small style="color:gray;"><s>{}</s></small>',
                discounted_str, original_str
            )
        else:
            return f"${float(obj.price):.2f}"

    discounted_price_display.short_description = "Chegirmali narx"
    discounted_price_display.admin_order_field = 'price'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'purchased_at', 'is_delivered')
    list_filter = ('is_delivered', 'purchased_at', 'product__category')
    search_fields = ('user__username', 'user__full_name', 'product__name')
    readonly_fields = ('user', 'product', 'quantity', 'total_price', 'purchased_at')
    list_editable = ('is_delivered',)

    def has_add_permission(self, request):
        return False