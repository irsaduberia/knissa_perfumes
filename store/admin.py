from django.contrib import admin
from .models import (
    Fragrance,
    Variant,
    Offer,
    Order,
    OrderItem,
    SiteSettings,
    SliderImage,
    About,
    PaymentQR
)

# ================================
# VARIANT INLINE (INSIDE FRAGRANCE)
# ================================
class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    fields = ('size', 'mrp', 'selling_price', 'is_active')


# ================================
# FRAGRANCE ADMIN
# ================================
@admin.register(Fragrance)
class FragranceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    inlines = [VariantInline]

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


# ================================
# VARIANT ADMIN
# ================================
@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('fragrance', 'size', 'mrp', 'selling_price', 'is_active')
    list_filter = ('size', 'is_active')
    search_fields = ('fragrance__name',)


# ================================
# OFFER ADMIN
# ================================
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer_price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)


# ================================
# ORDER ITEM INLINE
# ================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'size', 'price', 'quantity')


# ================================
# ORDER ADMIN
# ================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'total_amount',
        'status',
        'created_at'
    )

    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone')

    readonly_fields = (
        'full_name',
        'phone',
        'email',
        'address',
        'total_amount',
        'payment_method',
        'created_at'
    )

    inlines = [OrderItemInline]


# ================================
# SIMPLE MODELS
# ================================
admin.site.register(SiteSettings)
admin.site.register(SliderImage)
admin.site.register(About)
admin.site.register(PaymentQR)