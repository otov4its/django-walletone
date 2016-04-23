Install
=======

Install using pip:

.. code-block:: bash

    pip install django-walletone

Add application to INSTALLED_APPS:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'walletone.apps.DjangoWalletoneConfig',
        # ...
    ]

Settings:

.. code-block:: python

    # Online store ID (account number)
    # received at registration
    DJANGO_W1_MERCHANT_ID = '123456789012'

    # EDS creation method
    DJANGO_W1_SIGN_METHOD = 'md5'

    # Secret key from your W1 account
    DJANGO_W1_SECRET_KEY = 'sekret key'

    # Online store web-pages addresses (URL),
    # where buyer will be directed after successful
    # or unsuccessful payment.
    DJANGO_W1_SUCCESS_URL = 'https://your.domain/payment/success/'
    DJANGO_W1_FAIL_URL = 'https://your.domain/payment/fail/'

    # Currency ID (ISO 4217)
    # 643 — Russian Rubles
    # 840 — US Dollar
    # 978 — Euro
    # ...
    DJANGO_W1_CURRENCY_DEFAULT = '643'


Settings your root urls:

.. code-block:: python

    urlpatterns = [
        # ...
        url(r'^w1/', include('walletone.urls')),
        # ...
    ]

Update your database:

.. code-block:: bash

    ./manage.py migrate

