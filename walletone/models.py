import json

from django.db import models


class PaymentAttributeProxy(object):
    def __init__(self, payment):
        self._payment = payment

    def __getattr__(self, key):
        return self._get_data()[key]

    def __setattr__(self, key, value):
        if key == '_payment':
            super(PaymentAttributeProxy, self).__setattr__(key, value)
            return
        data = self._get_data()
        data[key] = value
        self._payment.extra_data = json.dumps(data)

    def _get_data(self):
        return dict(json.loads(self._payment.extra_data or '{}'))


class WalletOneSuccessPayment(models.Model):
    WMI_ORDER_ID = models.CharField(max_length=255, unique=True)
    WMI_MERCHANT_ID = models.CharField(max_length=255)
    WMI_PAYMENT_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)
    WMI_COMMISSION_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)
    WMI_CURRENCY_ID = models.IntegerField()
    WMI_TO_USER_ID = models.CharField(max_length=255, blank=True)
    WMI_PAYMENT_NO = models.CharField(max_length=255, blank=True)
    WMI_DESCRIPTION = models.CharField(max_length=255, blank=True)
    WMI_SUCCESS_URL = models.URLField(blank=True)
    WMI_FAIL_URL = models.URLField(blank=True)
    WMI_EXPIRED_DATE = models.DateTimeField(blank=True)
    WMI_CREATE_DATE = models.DateTimeField(blank=True)
    WMI_UPDATE_DATE = models.DateTimeField(blank=True)
    WMI_ORDER_STATE = models.CharField(max_length=255)

    extra_data = models.TextField(blank=True, default='{}')

    @property
    def extra_attrs(self):
        return PaymentAttributeProxy(self)