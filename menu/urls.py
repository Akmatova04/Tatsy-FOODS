# menu/urls.py
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Негизги барактар
    path('', views.home_view, name='home'),
    path('menu/', views.menu_list_view, name='menu_list'),
    path('menu/category/<slug:category_slug>/', views.menu_list_view, name='menu_list_by_category'),
    path('product/<slug:product_slug>/', views.product_detail_view, name='product_detail'),

    # Блог
    path('blog/', views.blog_list_view, name='blog_list'),
    path('blog/<slug:blog_slug>/', views.blog_detail_view, name='blog_detail'),

    # Статикалык барактар
    path('about-us/', views.about_us_view, name='about_us'),
    path('contact-us/', views.contact_us_view, name='contact_us'),

    # ----- Пикирлер -----
    path('testimonials/', views.testimonial_list_view, name='testimonial_list'), # Пикирлердин тизмеси (өзүнчө барак)
    path('review/add/', views.add_review_view, name='add_review'), # Жаңы пикир кошуу (жалпы же товар үчүн)
    # -------------------

    # Аккаунт, Каттоо, Профиль
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('my-account/orders/', views.my_orders_view, name='my_orders'),
    path('my-account/orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('my-account/address/', views.address_view, name='address'), # Placeholder
    path('my-account/saved-foods/', views.saved_foods_view, name='saved_foods'),
    path('ajax/toggle-save-food/', views.toggle_save_food, name='toggle_save_food'),

    # Заказ берүү жана корзина
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/', views.view_cart_view, name='view_cart'),
    path('cart/update/', views.update_cart_item_view, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-complete/', views.order_complete_view, name='order_complete'),

    # "Order Online" кнопкасы үчүн
    path('order-online/', views.menu_list_view, name='order_online'),
]