# menu/forms.py
# ТОЛУК КОД

from django import forms
from django.utils.translation import gettext_lazy as _
# Моделдерди импорттоо
from .models import ContactMessage, Order, Review # Review кошуу

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        labels = { 'name': _('Сиздин атыңыз'), 'email': _('Сиздин Email'), 'subject': _('Тема'), 'message': _('Сиздин билдирүүңүз'), }
        widgets = { 'name': forms.TextInput(attrs={'placeholder': _('Атыңызды бул жерге жазыңыз'), 'class': 'form-control'}), 'email': forms.EmailInput(attrs={'placeholder': _('email@example.com'), 'class': 'form-control'}), 'subject': forms.TextInput(attrs={'placeholder': _('Каттын темасы'), 'class': 'form-control'}), 'message': forms.Textarea(attrs={'placeholder': _('Билдирүүңүздүн текстин жазыңыз...'), 'rows': 5, 'class': 'form-control'}), }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code']
        labels = { 'first_name': _('Атыңыз'), 'last_name': _('Фамилияңыз'), 'email': _('Email (милдеттүү эмес)'), 'phone': _('Телефон номериңиз'), 'address': _('Жеткирүү дареги'), 'city': _('Шаар'), 'postal_code': _('Почта индекси (милдеттүү эмес)'), }
        widgets = { 'first_name': forms.TextInput(attrs={'placeholder': _('Мисалы: Асан'), 'class': 'form-control'}), 'last_name': forms.TextInput(attrs={'placeholder': _('Мисалы: Үсөнов'), 'class': 'form-control'}), 'email': forms.EmailInput(attrs={'placeholder': _('email@example.com'), 'class': 'form-control'}), 'phone': forms.TextInput(attrs={'placeholder': _('+996 XXX XXXXXX'), 'class': 'form-control'}), 'address': forms.TextInput(attrs={'placeholder': _('Көчө, үй номери, батир'), 'class': 'form-control'}), 'city': forms.TextInput(attrs={'placeholder': _('Мисалы: Бишкек'), 'class': 'form-control'}), 'postal_code': forms.TextInput(attrs={'placeholder': _('Мисалы: 720000'), 'class': 'form-control'}), }

# ----- ЖАҢЫ ПИКИР КАЛТЫРУУ ФОРМАСЫ -----
class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label=_("Сиздин бааңыз"),
        # 5тен 1ге чейинки тандоолор
        choices=[(i, f"{i} ★") for i in range(5, 0, -1)],
        # Радио баскычтар катары көрсөтүү
        widget=forms.RadioSelect(attrs={'class': 'star-rating-radio'}), # CSS үчүн класс
        required=False # Рейтинг милдеттүү эмес
    )

    class Meta:
        model = Review
        # Колдонуучу кирген болсо, author_name кереги жок
        fields = ['author_name', 'text', 'rating']
        labels = {
            'author_name': _('Сиздин атыңыз'),
            'text': _('Сиздин пикириңиз'),
            # 'rating' label'и ChoiceField'де аныкталды
        }
        widgets = {
            'author_name': forms.TextInput(attrs={'placeholder': _('Атыңызды жазыңыз'), 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'placeholder': _('Бул жерге пикириңизди жазыңыз...'), 'rows': 4, 'class': 'form-control'}),
            # Рейтинг үчүн виджетти ChoiceField өзү аныктайт (RadioSelect)
        }
        help_texts = {
             'author_name': _('Эгер сайтка кирген болсоңуз, бул талааны толтуруунун кажети жок.'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Көрүнүштөн user'ды алуу
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            if 'author_name' in self.fields:
                 # Ат талаасын жашырып, милдеттүү эмес кылуу
                 self.fields['author_name'].widget = forms.HiddenInput()
                 self.fields['author_name'].required = False
        else:
             # Катталбаган колдонуучу үчүн ат милдеттүү
             if 'author_name' in self.fields:
                 self.fields['author_name'].required = True
# --------------------------------------