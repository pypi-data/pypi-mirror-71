import os

SECRET_KEY = 'super-secret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    },
}

INSTALLED_APPS = [
    'django_markup',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
            ],
        },
    },
]
