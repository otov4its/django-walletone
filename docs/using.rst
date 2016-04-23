Using
=====

Payment form
------------

In order to simplify building payment form django-walletone
has the ``WalletOnePaymentForm``. It is necessary to simplify rendering
information in the templates and signature field calculation.

For example:

.. code-block:: python

    from walletone.models import WalletOneSuccessPayment

    def payment_form_example(request):
        form = WalletOnePaymentForm(initial={
            'WMI_PAYMENT_AMOUNT': '99.00',
            'WMI_DESCRIPTION': 'Order fro what?',
            'WMI_PAYMENT_NO': '1',
            'EXTRA_FIELD': 'value',
        })

        return render(
            request,
            'payment_form.html',
            {'form': form}
        )

.. note::
    You can use here any form field from `W1 docs <https://www.walletone.com/en/merchant/documentation/#step2>`_
    and any extra field just typing it in form's initial.

.. warning::
    | Notice that for now you can't use multiple values for form field like ``WMI_PTENABLED`` and ``WMI_PTDISABLED``.
    |
    | You can set only one value for ``WMI_PTENABLED`` and only one value for ``WMI_PTDISABLED``.
    |
    | It's alpha version. Sorry :)

The corresponding template ``payment_form.html``:

.. code-block:: html

    <form action="{{ form.action_url }}" method="POST" accept-charset="UTF-8">
      <p>{{ form.as_p }}</p>
      <p><input type="submit" value="Buy"></p>
    </form>

.. note::
    | The form is rendered as a set of input hidden tags.
    |
    | The form has a ``action_url`` attribute that contains the correct W1 processing URL.
    |
    | Notice ``accept-charset="UTF-8"``. It is better to **always** set.
    |
    | Note that ``{% csrf_token %}`` no needed here.


Getting paid results
--------------------

From official docs:

*Once the buyer completes the payment order, Wallet One Checkout performs
POST-request to the "Data to send the results of transaction", indicated
the in the online store settings. This request contains parameters of the payment
form, information about the result of payment and some additional parameters.*

So if you set your urls like:

.. code-block:: python

    urlpatterns = [
        url(r'^w1/', include('walletone.urls')),
    ]

you need to set "Data to send the results of transaction"::

    https://your.domain/w1/confirm/

After POST request from W1 app saves information about success payment
into the database (see model ``WalletOneSuccessPayment``) and generates signal (see below `Signals`_).

What if I send to W1 some extra fields? For example "EXTRA_FIELD1" and "EXTRA_FIELD2".
How can I retrieve it from my database? Very simple. Each ``WalletOneSuccessPayment``
instance has the ``extra_attrs`` attibute. For instance to get above attr just access
it like any other python attribute:

.. code-block:: python

    payment.extra_attrs.EXTRA_FIELD1
    payment.extra_attrs.EXTRA_FIELD2


Signals
-------

django-walletone sends ``payment_received`` singal after success confirmation from W1
and after saving information to a database.
``payment_received`` signal provides ``payment`` arg contains all information about payment.

Example:

.. code-block:: python

    from walletone.signals import payment_received
    from walletone.models import WalletOneSuccessPayment

    def receiver(**kwargs):
        payment = kwargs['payment']
        assert payment ==
            WalletOneSuccessPayment.objects \
            .get(WMI_ORDER_ID=payment.WMI_ORDER_ID)

    payment_received.connect(receiver)

