SECRET_KEY = 'FAKE_SECRET_KEY'

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = [
    'walletone.apps.DjangoWalletoneConfig',
    'django_nose',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

DJANGO_W1_MERCHANT_ID = '165531803223'
DJANGO_W1_SIGN_METHOD = 'md5'
DJANGO_W1_SECRET_KEY = '4d5a4a676d6634706c4e3742536d5344586c70456942325e425c77'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=walletone',
    '--cover-inclusive',
    '--verbosity=1',
]