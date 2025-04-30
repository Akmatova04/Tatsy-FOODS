# tastyfoods_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ----- Django'нун Аутентификация URL'дерин кошуу -----
    # Бул /accounts/login/, /accounts/logout/, /accounts/password_change/ ж.б. камсыздайт
    path('accounts/', include('django.contrib.auth.urls')),
    # -------------------------------------------------

    # Биздин 'menu' тиркемесинин URL'дерин кошуу
    path('', include('menu.urls', namespace='menu')),
]

# DEBUG режиминде медиа файлдарды көрсөтүү
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Эгер staticfiles_urlpatterns мурун кошкон болсоңуз, алып салсаңыз болот,
    # анткени AppDirectoriesFinder эми иштеп жатат.
    # from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # urlpatterns += staticfiles_urlpatterns()