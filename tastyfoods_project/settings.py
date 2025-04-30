# tastyfoods_project/settings.py

from pathlib import Path
import os # os импортун кошуу

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w5f4a_ot%ev&-_zjjd-a*)zyx_!*#5-p*n=fb)$xw5u9c83-9%' # Бул сиздин чыныгы ачкычыңыз менен алмаштырылышы керек

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menu', # Биздин тиркеме
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ---- LocaleMiddleware КОШУЛДУ (CommonMiddleware'ден мурун) ----
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ------------------------------------------------------------
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tastyfoods_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Долбоордун негизги папкасындагы templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # DEBUG үчүн кошуп койгон оң
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ---- i18n үчүн контекст процессорун кошуу (милдеттүү эмес, бирок пайдалуу) ----
                'django.template.context_processors.i18n',
                # -------------------------------------------------------------------------
            ],
        },
    },
]

WSGI_APPLICATION = 'tastyfoods_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

# ---- i18n/l10n Орнотуулары ----
LANGUAGE_CODE = 'ky' # Негизги тил - Кыргызча

TIME_ZONE = 'Asia/Bishkek' # Кыргызстандын убакыт алкагы

USE_I18N = True # Эл аралыкташтырууну иштетүү

USE_L10N = True # Локалдаштырууну иштетүү (дата/сан форматтары)

USE_TZ = True # Убакыт алкактарын колдонуу

# Котормо файлдарынын жайгашкан жери
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Сайтта жеткиликтүү тилдер (мисал)
LANGUAGES = [
    ('ky', 'Кыргызча'),
    # ('en', 'English'),
    # ('ru', 'Русский'),
]
# -------------------------------


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

# ----- Staticfiles Finders (Эгер мурун кошкон болсоңуз) -----
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder', # Бул маанилүү!
]
# ---------------------------------------------------------


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Auth URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'