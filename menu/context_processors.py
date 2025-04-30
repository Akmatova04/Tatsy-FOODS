# menu/context_processors.py
from .models import Category # Категориялар үчүн да кошобуз

def common_context(request):
    cart = request.session.get('cart', {})
    cart_item_count = 0
    for item_data in cart.values():
        cart_item_count += item_data.get('quantity', 0)

    # Активдүү категорияларды да кошолу (футерде колдонуу үчүн)
    active_categories = Category.objects.filter(is_active=True)

    return {
        'cart_item_count': cart_item_count,
        'active_categories': active_categories,
    }