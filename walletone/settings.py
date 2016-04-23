from django.conf import settings


MERCHANT_ID = getattr(settings, 'DJANGO_W1_MERCHANT_ID', '')

SIGN_METHOD = getattr(settings, 'DJANGO_W1_SIGN_METHOD', None)

SECRET_KEY = getattr(settings, 'DJANGO_W1_SECRET_KEY', '')

SUCCESS_URL = getattr(settings, 'DJANGO_W1_SUCCESS_URL', '')

FAIL_URL = getattr(settings, 'DJANGO_W1_FAIL_URL', '')

CURRENCY_DEFAULT = getattr(settings, 'DJANGO_W1_CURRENCY_DEFAULT', '643')

FORM_ACTION_URL = getattr(
    settings, 'DJANGO_W1_FORM_ACTION_URL',
    'https://wl.walletone.com/checkout/checkout/Index')
