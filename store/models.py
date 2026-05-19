from django.db import models
from django.utils.text import slugify


class Fragrance(models.Model):
    CATEGORY_CHOICES = [
        ('him', 'For Him'),
        ('her', 'For Her'),
        ('unisex', 'Unisex'),
        ('oud', 'Oud'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='fragrances/', blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    top_notes = models.CharField(max_length=255, blank=True)
    middle_notes = models.CharField(max_length=255, blank=True)
    base_notes = models.CharField(max_length=255, blank=True)

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Variant(models.Model):
    SIZE_CHOICES = (
        ('30', '30 ML'),
        ('100', '100 ML'),
    )

    fragrance = models.ForeignKey(
        Fragrance,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    mrp = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('fragrance', 'size')

    def __str__(self):
        return f"{self.fragrance.name} - {self.size} ML"


class Offer(models.Model):
    SIZE_CHOICES = (
        ('30', '30 ML'),
        ('100', '100 ML'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    min_quantity = models.PositiveIntegerField()

    applicable_size = models.CharField(
        max_length=3,
        choices=SIZE_CHOICES,
        blank=True,
        null=True
    )

    offer_price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    variant = models.ForeignKey(
        'Variant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    product_name = models.CharField(max_length=200)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name} ({self.size})"


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logo/')
    site_name = models.CharField(max_length=100, default="K-Nissa")

    def __str__(self):
        return "Site Settings"


class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='slider/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Slider Image"


class About(models.Model):
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='about/')

    def __str__(self):
        return "About Section"


class PaymentQR(models.Model):
    image = models.ImageField(upload_to='qr_codes/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Payment QR"