# menu/admin.py
# ТОЛУК КОД

from django.contrib import admin
# Order, OrderItem, Review кошуу
from .models import Category, Product, BlogPage, ContactMessage, Order, OrderItem, Review
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

# --- Категория Админ ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active'); list_filter = ('is_active',); search_fields = ('name',); prepopulated_fields = {'slug': ('name',)}; list_editable = ('is_active',)

# --- Товар Админ ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'is_active', 'display_saved_count', 'created_at'); list_filter = ('category', 'is_active', 'rating', 'created_at'); search_fields = ('name', 'description'); list_editable = ('price', 'rating', 'is_active'); prepopulated_fields = {'slug': ('name',)}; readonly_fields = ('created_at', 'updated_at'); filter_horizontal = ('saved_by',)
    fieldsets = ( (None, {'fields': ('name', 'slug', 'category', 'description', 'price', 'image')}), (_('Рейтинг, Скидка жана Активдүүлүк'), {'fields': ('rating', 'discount_percentage', 'discount_message', 'is_active')}), (_('Сактагандар'), {'fields': ('saved_by',)}), (_('Даталар'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}), )
    def display_saved_count(self, obj): return obj.saved_by.count(); display_saved_count.short_description = _("Сактагандар")

# --- Блог Админ ---
@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'is_published'); list_filter = ('is_published', 'author', 'publish_date'); search_fields = ('title', 'content'); prepopulated_fields = {'slug': ('title',)}; readonly_fields = ('created_at', 'updated_at'); list_editable = ('is_published',); date_hierarchy = 'publish_date'
    fieldsets = ( (None, {'fields': ('title', 'slug', 'author', 'image', 'content')}), (_('Жарыялоо'), {'fields': ('publish_date', 'is_published')}), (_('Даталар'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}), )
    def save_model(self, request, obj, form, change):
        if not obj.author_id: obj.author = request.user
        super().save_model(request, obj, form, change)

# --- Байланыш Билдирүү Админ ---
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'sent_at', 'is_read'); list_filter = ('is_read', 'sent_at'); search_fields = ('name', 'email', 'subject', 'message'); readonly_fields = ('name', 'email', 'subject', 'message', 'sent_at'); list_editable = ('is_read',); date_hierarchy = 'sent_at'

# --- OrderItem Inline ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem; raw_id_fields = ['product']; readonly_fields = ('price', 'get_cost_display'); extra = 0
    def get_cost_display(self, obj): return f"{obj.get_cost()} сом"; get_cost_display.short_description = _("Жалпы баасы") # Сомго өзгөртүү

# --- Order Admin ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'city', 'paid', 'status', 'created_at', 'display_total_cost'); list_filter = ('paid', 'status', 'created_at', 'updated_at'); search_fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'address'); list_editable = ('paid', 'status'); readonly_fields = ('created_at', 'updated_at', 'user_link', 'display_total_cost'); inlines = [OrderItemInline]
    fieldsets = ( (_("Кардар Маалыматы"), {'fields': ('user_link', ('first_name', 'last_name'), ('email', 'phone'))}), (_("Жеткирүү Дареги"), {'fields': ('address', 'city', 'postal_code')}), (_("Заказ Маалыматы"), {'fields': ('status', 'paid', 'display_total_cost')}), (_("Даталар"), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}), )
    def user_link(self, obj):
        if obj.user: link = reverse("admin:auth_user_change", args=[obj.user.id]); return format_html('<a href="{}">{}</a>', link, obj.user.username)
        return "-"; user_link.short_description = _('Колдонуучу')
    def display_total_cost(self, obj): return f"{obj.get_total_cost()} сом"; display_total_cost.short_description = _("Жалпы сумма") # Сомго өзгөртүү

# ----- ЖАҢЫ ПИКИРЛЕР АДМИН -----
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_author_display', 'product_display', 'rating', 'is_approved', 'is_featured', 'created_at')
    list_filter = ('is_approved', 'is_featured', 'rating', 'created_at', 'product')
    list_editable = ('is_approved', 'is_featured') # Админкадан тез жактыруу/белгилөө
    search_fields = ('text', 'author_name', 'user__username', 'product__name')
    # Админкадан түзөтүүгө мүмкүн болгон талаалар (эгер керек болсо)
    # fields = ('product', 'user', 'author_name', 'text', 'rating', 'is_approved', 'is_featured', 'created_at')
    # readonly_fields = ('created_at',) # Мисалы, түзүлгөн датаны гана өзгөртпөө

    # Көрсөтүү үчүн жардамчы функциялар
    def get_author_display(self, obj): return obj.get_author_name(); get_author_display.short_description = _('Автор'); get_author_display.admin_order_field = 'user'
    def product_display(self, obj): return obj.product.name if obj.product else "-"; product_display.short_description = _('Товар'); product_display.admin_order_field = 'product'

    # Админкада жапырт жактыруу/жактырбоо аракеттери (милдеттүү эмес)
    actions = ['approve_reviews', 'disapprove_reviews', 'feature_reviews', 'unfeature_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = _("Тандалган пикирлерди жактыруу")

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = _("Тандалган пикирлерди жактырбоо")

    def feature_reviews(self, request, queryset):
        queryset.update(is_featured=True)
    feature_reviews.short_description = _("Тандалган пикирлерди башкы бетке чыгаруу")

    def unfeature_reviews(self, request, queryset):
        queryset.update(is_featured=False)
    unfeature_reviews.short_description = _("Тандалган пикирлерди башкы беттен алуу")
# --------------------------------