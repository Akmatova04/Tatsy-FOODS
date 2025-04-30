
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import traceback

# Аутентификация үчүн импорттор
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Моделдерди импорттоо
from .models import Product, Category, BlogPage, ContactMessage, Order, OrderItem, Review
# Формаларды импорттоо
try:
    from .forms import ContactForm, CheckoutForm, ReviewForm
except ImportError:
    ContactForm = None; CheckoutForm = None; ReviewForm = None
    print("ЭСКЕРТҮҮ: menu/forms.py табылган жок же керектүү формалар жок.")

# --- Жардамчы функция (is_saved статусу үчүн) ---
def add_is_saved_status_to_products(request, product_list):
    if request.user.is_authenticated:
        saved_product_ids = set(request.user.saved_products.values_list('id', flat=True))
        for product in product_list: product.is_saved_by_user = product.id in saved_product_ids
    else:
        for product in product_list: product.is_saved_by_user = False
    return product_list

# --- Негизги Барактар ---
def home_view(request):
    latest_products_qs = Product.objects.filter(is_active=True).order_by('-created_at')[:6]
    categories = Category.objects.filter(is_active=True)
    latest_blog = BlogPage.objects.filter(is_published=True).order_by('-publish_date').first()
    latest_products = add_is_saved_status_to_products(request, list(latest_products_qs))
    featured_reviews = Review.objects.filter(is_approved=True, is_featured=True).select_related('user', 'product')[:5]
    context = { 'latest_products': latest_products, 'categories': categories, 'latest_blog': latest_blog, 'featured_reviews': featured_reviews, 'page_title': _("Башкы барак"), 'active_nav': 'home' }
    return render(request, 'menu/home.html', context)

def menu_list_view(request, category_slug=None):
    category = None; categories = Category.objects.filter(is_active=True); products_qs = Product.objects.filter(is_active=True).order_by('name')
    if category_slug: category = get_object_or_404(Category, slug=category_slug, is_active=True); products_qs = products_qs.filter(category=category); page_title = _("Меню: %(category_name)s") % {'category_name': category.name}
    else: page_title = _("Биздин Меню")
    products = add_is_saved_status_to_products(request, list(products_qs))
    context = { 'products': products, 'categories': categories, 'current_category': category, 'page_title': page_title, 'active_nav': 'menu' }
    return render(request, 'menu/menu_list.html', context)

def product_detail_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True); categories = Category.objects.filter(is_active=True)
    related_products_qs = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    is_saved = False
    if request.user.is_authenticated: is_saved = product.saved_by.filter(pk=request.user.pk).exists()
    related_products = add_is_saved_status_to_products(request, list(related_products_qs))
    product_reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')
    average_rating = product_reviews.aggregate(Avg('rating'))['rating__avg']
    review_form = ReviewForm(user=request.user) if ReviewForm else None
    context = { 'product': product, 'categories': categories, 'related_products': related_products, 'is_saved': is_saved, 'product_reviews': product_reviews, 'average_rating': average_rating, 'review_form': review_form, 'page_title': product.name, 'active_nav': 'menu' }
    return render(request, 'menu/product_detail.html', context)

# --- Блог Барактары ---
def blog_list_view(request):
    blog_posts = BlogPage.objects.filter(is_published=True).order_by('-publish_date')
    categories = Category.objects.filter(is_active=True)
    context = { 'blog_posts': blog_posts, 'categories': categories, 'page_title': _("Блог"), 'active_nav': 'blog' }
    return render(request, 'menu/blog_list.html', context)
def blog_detail_view(request, blog_slug):
    blog_post = get_object_or_404(BlogPage, slug=blog_slug, is_published=True); categories = Category.objects.filter(is_active=True)
    recent_posts = BlogPage.objects.filter(is_published=True).exclude(pk=blog_post.pk).order_by('-publish_date')[:5]
    context = { 'post': blog_post, 'categories': categories, 'recent_posts': recent_posts, 'page_title': blog_post.title, 'active_nav': 'blog' }
    return render(request, 'menu/blog_detail.html', context)

# --- Статикалык Барактар ---
def about_us_view(request):
    categories = Category.objects.filter(is_active=True)
    context = { 'page_title': _("Биз жөнүндө"), 'active_nav': 'about', 'categories': categories, }
    return render(request, 'menu/about.html', context)
def contact_us_view(request):
    categories = Category.objects.filter(is_active=True)
    if ContactForm is None: messages.error(request, _("Байланыш формасы азырынча жеткиликсиз.")); form = None
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): form.save(); messages.success(request, ('Сиздин билдирүүңүз ийгиликтүү жөнөтүлдү!')); return redirect('menu:contact_us')
        else: messages.error(request, _('Форманы толтурууда ката кетти.'))
    else: form = ContactForm()
    context = { 'form': form, 'page_title': _("Байланыш"), 'active_nav': 'contact', 'categories': categories, }
    return render(request, 'menu/contact.html', context)

# ==================== АУТЕНТИФИКАЦИЯ ЖАНА АККАУНТ ====================
def register_view(request):
    if request.user.is_authenticated: return redirect('menu:home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): user = form.save(); login(request, user); messages.success(request, _("Сиз ийгиликтүү катталдыңыз!")); return redirect('menu:home')
        else: messages.error(request, _("Каттоо формасында каталар бар. Сураныч, текшериңиз."))
    else: form = UserCreationForm()
    context = { 'form': form, 'page_title': _("Каттоо"), 'active_nav': 'register' }
    return render(request, 'registration/register.html', context)

@login_required
def profile_view(request):
    user = request.user; categories = Category.objects.filter(is_active=True)
    context = { 'page_title': _("Менин Профилим"), 'active_nav': 'my_account', 'categories': categories, }
    return render(request, 'menu/profile.html', context)

@login_required
def saved_foods_view(request):
    saved_products_qs = request.user.saved_products.filter(is_active=True).order_by('-created_at')
    saved_products = add_is_saved_status_to_products(request, list(saved_products_qs))
    categories = Category.objects.filter(is_active=True)
    context = { 'saved_products': saved_products, 'page_title': _("Сакталган тамактар"), 'active_nav': 'saved_foods', 'categories': categories, }
    return render(request, 'menu/saved_foods.html', context)

@login_required
@require_POST
def toggle_save_food(request):
    product_id = request.POST.get('product_id'); action = request.POST.get('action')
    if not product_id or not action: return JsonResponse({'status': 'error', 'message': _('Маалымат жетишсиз')}, status=400)
    try: product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist: return JsonResponse({'status': 'error', 'message': _('Товар табылган жок')}, status=404)
    user = request.user; saved = False
    if action == 'save': product.saved_by.add(user); saved = True; message = _("'%(product_name)s' сакталды.") % {'product_name': product.name}
    elif action == 'unsave': product.saved_by.remove(user); saved = False; message = _("'%(product_name)s' сакталгандардан өчүрүлдү.") % {'product_name': product.name}
    else: return JsonResponse({'status': 'error', 'message': _('Белгисиз аракет')}, status=400)
    return JsonResponse({'status': 'ok', 'saved': saved, 'message': message})

@login_required
def my_orders_view(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    categories = Category.objects.filter(is_active=True)
    context = { 'orders': user_orders, 'page_title': _("Менин Заказдарым"), 'active_nav': 'my_orders', 'categories': categories, }
    return render(request, 'menu/my_orders.html', context)

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all().select_related('product')
    categories = Category.objects.filter(is_active=True)
    context = { 'order': order, 'order_items': order_items, 'page_title': _("Заказдын Деталдары") + f" #{order.id}", 'active_nav': 'my_orders', 'categories': categories, }
    return render(request, 'menu/order_detail.html', context)

@login_required
def address_view(request):
    context = {'page_title': _("Даректер"), 'active_nav': 'address'}
    messages.info(request, _("Даректерди башкаруу функциясы азырынча иштебейт."))
    return render(request, 'menu/placeholder_page.html', context)

# ==================== КОРЗИНА ЖАНА ЗАКАЗ ЛОГИКАСЫ ====================
# ... (add_to_cart_view, view_cart_view, update_cart_item_view, remove_from_cart_view өзгөрүүсүз) ...
@require_POST
def add_to_cart_view(request, product_id):
    cart = request.session.get('cart', {}); product_id_str = str(product_id)
    try: product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist: messages.error(request, _("Товар табылган жок же активдүү эмес.")); return redirect(request.META.get('HTTP_REFERER', 'menu:home'))
    quantity = 1
    if product_id_str in cart: messages.info(request, _("'%(product_name)s' мурунтан эле корзинада.") % {'product_name': product.name})
    else: cart[product_id_str] = {'quantity': quantity, 'price': str(product.price)}; messages.success(request, _("'%(product_name)s' корзинага кошулду.") % {'product_name': product.name}); request.session['cart'] = cart; request.session.modified = True
    return redirect('menu:view_cart')

def view_cart_view(request):
    cart = request.session.get('cart', {}); cart_products = []; total_price = Decimal('0.00')
    product_ids = cart.keys(); products_in_db = Product.objects.filter(id__in=product_ids, is_active=True); products_in_db_dict = {str(p.id): p for p in products_in_db}
    items_to_remove = []
    for product_id, item_data in cart.items():
        product = products_in_db_dict.get(product_id)
        if product: quantity = item_data.get('quantity', 0); 
        if quantity <= 0: items_to_remove.append(product_id); continue; price = Decimal(item_data.get('price', '0.00')); total_item_price = price * quantity; cart_products.append({ 'product': product, 'quantity': quantity, 'price': price, 'total_price': total_item_price, }); total_price += total_item_price
        else: items_to_remove.append(product_id)
    if items_to_remove:
        cart_changed = False
        for item_id in items_to_remove:
            if item_id in cart: del cart[item_id]; cart_changed = True
        if cart_changed: request.session['cart'] = cart; request.session.modified = True
    context = { 'cart_products': cart_products, 'total_price': total_price, 'page_title': _("Сиздин корзинаңыз"), 'active_nav': 'order' }
    return render(request, 'menu/cart.html', context)

@require_POST
def update_cart_item_view(request):
    product_id = request.POST.get('product_id'); change = request.POST.get('change')
    if not product_id or not change: return JsonResponse({'status': 'error', 'message': _('Маалымат жетишсиз.')}, status=400)
    try: change = int(change)
    except ValueError: return JsonResponse({'status': 'error', 'message': _('Жараксыз сан өзгөрүүсү.')}, status=400)
    cart = request.session.get('cart', {}); product_id_str = str(product_id)
    if product_id_str not in cart: return JsonResponse({'status': 'error', 'message': _('Товар корзинада табылган жок.')}, status=404)
    try:
        new_quantity = cart[product_id_str]['quantity'] + change; item_removed = False; item_total_price = Decimal('0.00')
        if new_quantity <= 0: del cart[product_id_str]; message = _("Товар корзинадан өчүрүлдү."); item_removed = True; new_quantity = 0
        else: new_quantity = min(new_quantity, 10); cart[product_id_str]['quantity'] = new_quantity; message = _("Товардын саны жаңыртылды."); item_price = Decimal(cart[product_id_str]['price']); item_total_price = item_price * new_quantity
        request.session['cart'] = cart; request.session.modified = True
        total_cart_price = Decimal('0.00'); cart_item_count = 0
        for item_data in cart.values(): total_cart_price += Decimal(item_data['price']) * item_data['quantity']; cart_item_count += item_data['quantity']
        return JsonResponse({ 'status': 'ok', 'message': message, 'item_removed': item_removed, 'new_quantity': new_quantity, 'item_total_price': str(item_total_price.quantize(Decimal("0.01"))), 'total_cart_price': str(total_cart_price.quantize(Decimal("0.01"))), 'cart_item_count': cart_item_count })
    except Exception as e: print(f"Update cart error: {e}"); traceback.print_exc(); return JsonResponse({'status': 'error', 'message': _('Санды жаңыртууда ката кетти.')}, status=500)

@require_POST
def remove_from_cart_view(request):
    product_id = request.POST.get('product_id');
    if not product_id: return JsonResponse({'status': 'error', 'message': _('Товардын IDси көрсөтүлгөн эмес.')}, status=400)
    cart = request.session.get('cart', {}); product_id_str = str(product_id); message = _('Товар корзинада табылган жок.'); cart_changed = False
    if product_id_str in cart:
        try: del cart[product_id_str]; request.session['cart'] = cart; request.session.modified = True; message = _("Товар корзинадан ийгиликтүү өчүрүлдү."); cart_changed = True
        except Exception as e: print(f"Remove from cart error: {e}"); traceback.print_exc(); return JsonResponse({'status': 'error', 'message': _('Товарды өчүрүүдө ката кетти.')}, status=500)
    total_cart_price = Decimal('0.00'); cart_item_count = 0
    for item_data in cart.values(): total_cart_price += Decimal(item_data['price']) * item_data['quantity']; cart_item_count += item_data['quantity']
    return JsonResponse({ 'status': 'ok', 'message': message, 'total_cart_price': str(total_cart_price.quantize(Decimal("0.01"))), 'cart_item_count': cart_item_count, 'cart_is_empty': cart_item_count == 0 })

def checkout_view(request):
    cart = request.session.get('cart', {});
    if not cart and request.method == 'GET': messages.warning(request, _("Заказ берүү үчүн алгач корзинага товар кошуңуз.")); return redirect('menu:view_cart')
    if CheckoutForm is None: messages.error(request, _("Заказ формасы азырынча жеткиликсиз.")); return redirect('menu:view_cart')
    if request.method == 'POST':
        form = CheckoutForm(request.POST); payment_method = request.POST.get('payment_method', 'cash')
        if form.is_valid():
            try:
                order = form.save(commit=False);
                if request.user.is_authenticated: order.user = request.user
                if payment_method == 'cash': order.paid = False; order.status = 'Pending'
                else: order.paid = False; order.status = 'Pending'
                order.save(); request.session['last_order_id'] = order.id
                product_ids = cart.keys(); products = Product.objects.filter(id__in=product_ids); product_map = {str(p.id): p for p in products}
                for product_id, item_data in cart.items():
                    product_obj = product_map.get(product_id)
                    if product_obj: OrderItem.objects.create( order=order, product=product_obj, price=Decimal(item_data['price']), quantity=item_data['quantity'] )
                if 'cart' in request.session: del request.session['cart']; request.session.modified = True
                if payment_method == 'cash': messages.success(request, _("Сиздин заказыңыз кабыл алынды! Курьерге накталай төлөңүз."))
                else: messages.success(request, _("Сиздин заказыңыз ийгиликтүү кабыл алынды!"))
                return redirect('menu:order_complete')
            except Exception as e: print(f"--- Checkout View КАТА (try-except ичинде): {e}"); traceback.print_exc(); messages.error(request, _("Заказды иштетүүдө күтүлбөгөн ката кетти.")); return redirect('menu:view_cart')
        else:
            messages.error(request, _("Сураныч, формадагы каталарды оңдоңуз."))
            cart_products = []; total_price = Decimal('0.00'); product_ids = cart.keys(); products_in_db = Product.objects.filter(id__in=product_ids, is_active=True); products_in_db_dict = {str(p.id): p for p in products_in_db}
            for product_id, item_data in cart.items(): product = products_in_db_dict.get(product_id)
            if product: quantity = item_data.get('quantity', 0); price = Decimal(item_data.get('price', '0.00')); total_item_price = price * quantity; cart_products.append({ 'product': product, 'quantity': quantity, 'price': price, 'total_price': total_item_price, }); total_price += total_item_price
    else: # GET сурамы
        initial_data = {};
        if request.user.is_authenticated: initial_data = { 'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email, }
        form = CheckoutForm(initial=initial_data)
        cart_products = []; total_price = Decimal('0.00'); product_ids = cart.keys(); products_in_db = Product.objects.filter(id__in=product_ids, is_active=True); products_in_db_dict = {str(p.id): p for p in products_in_db}
        items_to_remove = []
        for product_id, item_data in cart.items():
             product = products_in_db_dict.get(product_id)
             if product: quantity = item_data.get('quantity', 0)
             if quantity <= 0: items_to_remove.append(product_id); continue; price = Decimal(item_data.get('price', '0.00')); total_item_price = price * quantity; cart_products.append({ 'product': product, 'quantity': quantity, 'price': price, 'total_price': total_item_price, }); total_price += total_item_price
             else: items_to_remove.append(product_id)
        if items_to_remove: cart_changed = False
    for item_id in items_to_remove:
                if item_id in cart: del cart[item_id]; cart_changed = True
    if cart_changed: request.session['cart'] = cart; request.session.modified = True
    context = { 'form': form, 'cart_products': cart_products, 'total_price': total_price, 'page_title': _("Заказды тастыктоо"), 'active_nav': 'order' }
    return render(request, 'menu/checkout.html', context)

def order_complete_view(request):
     last_order_id = request.session.get('last_order_id', None)
     context = { 'page_title': _("Заказ кабыл алынды"), 'last_order_id': last_order_id, 'active_nav': 'order' }
     return render(request, 'menu/order_complete.html', context)

# ==================== ПИКИРЛЕР (ОТЗЫВ) ====================
def testimonial_list_view(request):
    reviews = Review.objects.filter(is_approved=True).select_related('user', 'product').order_by('-created_at')
    categories = Category.objects.filter(is_active=True)
    review_form = ReviewForm(user=request.user) if ReviewForm else None
    context = { 'reviews': reviews, 'review_form': review_form, 'page_title': _("Кардарлардын Пикирлери"), 'active_nav': 'testimonial', 'categories': categories, }
    return render(request, 'menu/testimonial_list.html', context)

@require_POST
def add_review_view(request):
    product_id = request.POST.get('product_id')
    product = None
    if product_id:
        try: product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist: messages.error(request, _("Пикир калтырыла турган товар табылган жок.")); return redirect(request.META.get('HTTP_REFERER', 'menu:home'))

    form = ReviewForm(request.POST, user=request.user)

    if form.is_valid():
        try:
            review = form.save(commit=False)
            review.product = product
            if request.user.is_authenticated: review.user = request.user

            # Рейтингди текшерүү жана коюу
            rating_value = form.cleaned_data.get('rating')
            if rating_value: review.rating = int(rating_value)
            else: review.rating = None # Эгер тандалбаса

            review.is_approved = False # Админ жактырышы керек
            review.save()
            messages.success(request, _("Пикириңиз үчүн рахмат! Ал текшерүүдөн кийин сайтка чыгарылат."))
            redirect_url = request.META.get('HTTP_REFERER', 'menu:home')
            if product: redirect_url = product.get_absolute_url() + '#reviews'
            return redirect(redirect_url)
        except Exception as e:
            print(f"--- Add Review КАТА (Сактоо учурунда): {type(e).__name__} - {e} ---")
            traceback.print_exc()
            messages.error(request, _("Пикирди сактоодо ката кетти."))
            return redirect(request.META.get('HTTP_REFERER', 'menu:home'))
    else:
        # Форма жараксыз болгондо каталарды көрсөтүү үчүн көбүрөөк маалымат кошуу
        error_message = _("Пикир формасында каталар бар:")
        for field, errors in form.errors.items():
             error_message += f" {field}: {', '.join(errors)}" # Каталарды тизмелөө
        messages.error(request, error_message)
        print("--- Add Review: Форма жараксыз (валидный эмес) ---")
        print("--- Add Review: Форма каталары:", form.errors.as_json())
        redirect_url = request.META.get('HTTP_REFERER', 'menu:home')
        # Товар барагы болсо, форма бөлүмүнө кайтуу (#review-form)
        if product: redirect_url = product.get_absolute_url() + '#review-form'
        return redirect(redirect_url)
# ==================== ПИКИРЛЕРДИН АЯГЫ ====================