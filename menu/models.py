# menu/models.py
# ТОЛУК КОД

from django.db import models
from django.contrib.auth.models import User # Стандарттык User модели
from django.conf import settings # AUTH_USER_MODEL алуу үчүн
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from decimal import Decimal # Бул жерде кереги жок, бирок калтыралы

# --- Категория Модели ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Категория аты"))
    slug = models.SlugField(max_length=110, unique=True, blank=True, verbose_name="Слаг (авто)")
    is_active = models.BooleanField(default=True, verbose_name=_("Активдүү"))

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name); slug = base_slug; counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists(): slug = f"{base_slug}-{counter}"; counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse('menu:menu_list_by_category', args=[self.slug])
    def __str__(self): return self.name
    class Meta: verbose_name = _("Категория"); verbose_name_plural = _("Категориялар"); ordering = ['name']

# --- Товар (Продукт) Модели ---
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Категория"))
    name = models.CharField(max_length=200, verbose_name=_("Аты"))
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name="Слаг (авто)")
    description = models.TextField(blank=True, null=True, verbose_name=_("Сүрөттөмө"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Баасы (сом)")) # Доллар эмес, сом
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_("Сүрөт"))
    rating = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0, verbose_name=_("Рейтинг (0-5)"))
    discount_percentage = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Скидка (%)"))
    discount_message = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Скидка билдирүүсү"))
    saved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saved_products', blank=True, verbose_name=_("Кимдер сактады"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активдүү (көрүнгөн)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Түзүлгөн дата"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Жаңыланган дата"))

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name); slug = base_slug; counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists(): slug = f"{base_slug}-{counter}"; counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse('menu:product_detail', args=[self.slug])
    def __str__(self): return self.name
    class Meta: verbose_name = _("Товар (Тамак)"); verbose_name_plural = _("Товарлар (Тамактар)"); ordering = ['-created_at']
    def has_discount(self): return self.discount_percentage is not None and self.discount_percentage > 0
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'): return self.image.url
        from django.templatetags.static import static; return static('menu/placeholder.png')
    # Орточо рейтингди эсептөөчү метод (керек болсо)
    def get_average_rating(self):
        return self.reviews.filter(is_approved=True).aggregate(('rating'))['rating__avg']

# --- Блог Модели ---
class BlogPage(models.Model):
    # ... (BlogPage модели өзгөрүүсүз) ...
    title = models.CharField(max_length=250, verbose_name=_("Аталышы"))
    slug = models.SlugField(max_length=270, unique=True, blank=True, verbose_name="Слаг (авто)")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts', verbose_name=_("Автор"))
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name=_("Сүрөт"))
    content = models.TextField(verbose_name=_("Мазмуну"))
    publish_date = models.DateTimeField(default=timezone.now, verbose_name=_("Жарыяланган датасы"))
    is_published = models.BooleanField(default=True, verbose_name=_("Жарыяланды"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs): # Slug генерациясы
        if not self.slug:
            base_slug = slugify(self.title); slug = base_slug; counter = 1
            while BlogPage.objects.filter(slug=slug).exclude(pk=self.pk).exists(): slug = f"{base_slug}-{counter}"; counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse('menu:blog_detail', args=[self.slug])
    def __str__(self): return self.title
    class Meta: verbose_name = _("Блог Барагы"); verbose_name_plural = _("Блог Барактары"); ordering = ['-publish_date']
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'): return self.image.url
        from django.templatetags.static import static; return static('menu/placeholder_blog.png')

# --- Байланыш Билдирүү Модели ---
class ContactMessage(models.Model):
    # ... (ContactMessage модели өзгөрүүсүз) ...
    name = models.CharField(max_length=100, verbose_name=_("Аты"))
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(max_length=200, verbose_name=_("Тема"))
    message = models.TextField(verbose_name=_("Билдирүү"))
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Жөнөтүлгөн убакыт"))
    is_read = models.BooleanField(default=False, verbose_name=_("Окулду"))
    def __str__(self): return f"Билдирүү: {self.subject} ({self.name})"
    class Meta: verbose_name = _("Байланыш Билдирүүсү"); verbose_name_plural = _("Байланыш Билдирүүлөрү"); ordering = ['-sent_at']

# --- Заказ Моделдери ---
class Order(models.Model):
    # ... (Order модели өзгөрүүсүз) ...
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Колдонуучу"))
    first_name = models.CharField(_("Аты"), max_length=100); last_name = models.CharField(_("Фамилиясы"), max_length=100)
    email = models.EmailField(_("Email"), blank=True); phone = models.CharField(_("Телефон номери"), max_length=20)
    address = models.CharField(_("Дареги"), max_length=250); postal_code = models.CharField(_("Почта индекси"), max_length=20, blank=True)
    city = models.CharField(_("Шаар"), max_length=100); created_at = models.DateTimeField(_("Түзүлгөн убакыт"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Жаңыланган убакыт"), auto_now=True); paid = models.BooleanField(_("Төлөндү"), default=False)
    STATUS_CHOICES = ( ('Pending', _('Күтүүдө')), ('Processing', _('Иштетүүдө')), ('Shipped', _('Жөнөтүлдү')), ('Delivered', _('Жеткирилди')), ('Cancelled', _('Жокко чыгарылды')), )
    status = models.CharField(_("Статус"), max_length=10, choices=STATUS_CHOICES, default='Pending')
    class Meta: ordering = ('-created_at',); verbose_name = _("Заказ"); verbose_name_plural = _("Заказдар")
    def __str__(self): return f"Заказ №{self.id}"
    def get_total_cost(self): return sum(item.get_cost() for item in self.items.all())
    def get_absolute_url(self): return reverse('menu:order_detail', args=[self.id])

class OrderItem(models.Model):
    # ... (OrderItem модели өзгөрүүсүз) ...
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_("Заказ"))
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name=_("Товар"))
    price = models.DecimalField(_("Баасы (заказ учурунда)"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Саны"), default=1)
    class Meta: verbose_name = _("Заказ Элементи"); verbose_name_plural = _("Заказ Элементтери")
    def __str__(self): return str(self.id)
    def get_cost(self): return self.price * self.quantity

# ----- ЖАҢЫ ПИКИР (ОТЗЫВ) МОДЕЛИ -----
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True, verbose_name=_("Товар"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Колдонуучу"))
    author_name = models.CharField(_("Автордун аты"), max_length=100, blank=True)
    text = models.TextField(_("Пикирдин тексти"))
    rating = models.PositiveSmallIntegerField( _("Рейтинг"), validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True )
    created_at = models.DateTimeField(_("Түзүлгөн убакыт"), auto_now_add=True)
    is_approved = models.BooleanField(_("Жактырылды"), default=False, help_text=_("Сайтта көрсөтүү үчүн белгилеңиз"))
    is_featured = models.BooleanField(_("Башкы бетте көрсөтүлөт"), default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Пикир")
        verbose_name_plural = _("Пикирлер")

    def __str__(self):
        author = self.user.username if self.user else self.author_name
        if self.product: return _("Пикир: %(author)s - %(product)s") % {'author': author, 'product': self.product.name}
        else: return _("Пикир: %(author)s (Жалпы сайт)") % {'author': author}

    def get_author_name(self):
        if self.user: return self.user.get_full_name() or self.user.username
        return self.author_name or _("Аноним")
# -----------------------------------------