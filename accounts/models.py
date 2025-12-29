from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# pip install django-phonenumbers bo‘lsa ishlaydi


class CustomUser(AbstractUser):
    """
    Zum platformasining asosiy foydalanuvchisi
    Balance bu yerda emas — wallet app’da!
    """
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # muhim!
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # muhim!
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    # Asosiy identifikatorlar (ikkalasi ham unique)
    phone_number = PhoneNumberField(
        region='UZ',                    # O‘zbekiston uchun default
        unique=True,
        blank=False,
        null=False,
        verbose_name="Telefon raqami",
        help_text="+998901234567 formatida"
    )

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Email"
    )

    # Pul jo‘natishda ishlatiladigan username (@akbar_07)
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Username",
        help_text="@ bilan ishlatiladi"
    )

    # To‘liq ismi
    full_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="F.I.Sh"
    )

    # Profil rasm
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Profil rasm",
        help_text="Yuklamasangiz default rasm qo‘yiladi"
    )

    # Django standart field’lari (o‘zgartirmaymiz)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Login qilishda username o‘rniga email yoki phone_number ishlatish uchun
    USERNAME_FIELD = 'username'        # login qilganda @username so‘raymiz
    REQUIRED_FIELDS = ['email', 'phone_number', 'full_name']  # createsuperuser da so‘raladi

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-date_joined']

    def __str__(self):
        return f"@{self.username} ({self.full_name})"

    # Profil sahifasida ko‘rsatish uchun qulay metodlar
    def get_short_name(self):
        return self.full_name.split()[0]

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/images/default-avatar.png"  # keyin qo‘shamiz