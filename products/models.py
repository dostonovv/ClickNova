# products/models.py — ZUM VALYUTASIZ, USD NARXLI FINAL VERSIYA
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator  # <--- YANGI QATOR
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug (url uchun)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Narxi (USD)"
    )

    stock = models.PositiveIntegerField(default=0, verbose_name="Qolgan soni")

    description = models.TextField(blank=True, verbose_name="Tavsif")

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Kategoriya"
    )

    # image = models.ImageField(
    #     upload_to='products/',
    #     blank=True,
    #     null=True,
    #     verbose_name="Asosiy rasm"
    # )

    is_active = models.BooleanField(default=True, verbose_name="Sotuvda")

    delivery_days = models.PositiveIntegerField(
        default=3,
        verbose_name="Yetkazib berish muddati (kun)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo‘shilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")


    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (${self.price})"

    def is_available(self):
        return self.is_active and self.stock > 0
    is_available.boolean = True
    is_available.short_description = "Mavjud"

    # products/models.py — Product ichiga qo‘sh (price dan keyin)
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Chegirma (%)"
    )
    def get_discounted_price(self):
        if self.discount_percent > 0:
            discount_amount = self.price * Decimal(str(self.discount_percent)) / Decimal('100')
            return self.price - discount_amount
        return self.price

    def get_original_price(self):
        return self.price

class Order(models.Model):
    STATUS_CHOICES = (
        ('accepted', 'Buyurtma qabul qilindi'),
        ('shipping', 'Yetkazilmoqda'),
        ('delivered', 'Yetkazib berildi'),
    )

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Umumiy narx (USD)")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan vaqt")
    is_delivered = models.BooleanField(default=False, verbose_name="Yetkazib berildi")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='accepted',
        verbose_name="Buyurtma holati")
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-purchased_at']

    def __str__(self):
        return f"{self.user.username} — {self.product.name} (${self.total_price})"


# products/models.py — oxiriga qo‘sh
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name="Rasm")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Rasm tavsifi")
    is_main = models.BooleanField(default=False, verbose_name="Asosiy rasm")

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"

    def __str__(self):
        return f"{self.product.name} - Rasm {self.id}"

    def save(self, *args, **kwargs):
        # Agar bu rasm asosiy bo‘lsa, boshqa rasmlarni asosiy emas qil
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)