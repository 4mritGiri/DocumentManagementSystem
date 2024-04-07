from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRONMENT = os.getenv('ENVIRONMENT', default='development')
if ENVIRONMENT == 'production':
    print("Production Environment...")
    DEBUG = False
    ALLOWED_HOSTS = ["dms.up.railway.app", ".vercel.app", ".now.sh"]
# else:
#     print("Development Environment...")
#     DEBUG = True
#     ALLOWED_HOSTS = ["127.0.0.1","localhost"]

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1","localhost", "dms.up.railway.app", ".vercel.app", ".now.sh"]

CSRF_TRUSTED_ORIGINS = ["https://dms.up.railway.app"]

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # local apps
    'Accounts.apps.AccountsConfig',
    # 'dmsApp.apps.DmsappConfig',
    'Package.apps.PackageConfig',
    'PackageCollection.apps.PackagecollectionConfig',
    'DestructionEligible.apps.DestructioneligibleConfig',
    'ScheduledMonitoring.apps.ScheduledmonitoringConfig', 
    'DocumentApps.apps.DocumentappsConfig',
    'dashboard.apps.DashboardConfig',
    'notifications.apps.NotificationsConfig',

    # for beat schedule
    'django_celery_beat', 
    'django_celery_results',

    # 3rd party apps
    'user_visit', # pip install 
]

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "DMS",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "DMS",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "DMS",

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "default/logo.png",
    "site_logo": "../media/default/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "assets/media/logos/dmss.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "assets/media/logos/dmss.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "../media/default/logo.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome DMS",

    # Copyright on the footer
    "copyright": "DMS",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "auth.User",
    # "search_model": "Package.Package",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    # ImageField
    'user_avatar': None,


    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        # {"name": "Messages", "url": "admin:make_messages", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},

        # external url that opens in a new window (Permissions can be added)
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "Package.Package"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Github", "url": "https://github.com/4mritGiri/DocumentManagementSystem" , "new_window": True, "icon": "fab fa-github"},
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth","Package"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
    },
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "Package": "fas fa-box-open",
        "Package.Package": "fas fa-box-open",
        "Package.Document": "fas fa-file-alt",
        "Package.Branch": "fas fa-code-branch",
        "Package.Compartment": "fas fa-warehouse",
        "Package.Rack": "fas fa-warehouse",
        "Package.StoreRoom": "fas fa-store",
        "Package.PackageVerification": "fas fa-address-card",
        "dmsApp.Post": "fab fa-telegram-plane",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # # - carousel
    # "changeform_format": "carousel",
    # # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
    "show_ui_builder" : True
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
]

ROOT_URLCONF = 'DocumentManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'Package.global_context.global_context',
                'notifications.notifications_context.notifications_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'DocumentManagementSystem.wsgi.application'
ASGI_APPLICATION = 'DocumentManagementSystem.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'dbaa.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL Database Configuration for Production in vercel
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": os.environ.get("DMS_DATABASE"),
#         "USER": os.environ.get("DMS_USER"),
#         "PASSWORD": os.environ.get("DMS_PASSWORD"),
#         "HOST": os.environ.get("DMS_HOST"),
#         "PORT": os.environ.get("DMS_PORT"),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files (uploads, user uploads, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/login'

# STATICFILES_DIRS = [os.path.join(BASE_DIR, "ui/static")]
# STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "ui/staticfiles")

ID_ENCRYPTION_KEY = b'UdhnfelTxqj3q6BbPe7H86sfQnboSBzb0irm2atoFUw='

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_USER_MODEL = 'Accounts.CustomUser'


    # ***********************************
    # * DJANGO-CHANELS STUFF (Settings) *
    # ***********************************
# ======================= CHANNEL_LAYERS =============================== 

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

    # *********************
    # * CELERY (Settings) *
    # *********************
# ============================= CELERY STUFF =============================
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CELERY_BEAT_SCHEDULE = {
#     'scheduled_monitoring': {
#         'task': 'ScheduledMonitoring.tasks.scheduled_monitoring',
#         'schedule': 60.0,
#     },
# }

# # celery setting.
# CELERY_CACHE_BACKEND = 'default'

# # django setting.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_cache_table',
#     }
# }

