# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from decimal import Decimal

from django.test import TestCase

from walletone.models import (
    WalletOneSuccessPayment, PaymentAttributeProxy
)


class SuccessPaymentModelTestCase(TestCase):
    def setUp(self):
        self.data = {
            'WMI_ORDER_ID': '336077917075',
            'WMI_MERCHANT_ID': '165531803223',
            'WMI_PAYMENT_AMOUNT': Decimal('1.00'),
            'WMI_COMMISSION_AMOUNT': Decimal('0.00'),
            'WMI_CURRENCY_ID': 643,
            'WMI_PAYMENT_NO': '1',
            'WMI_DESCRIPTION': 'Мой тестовый заказ',
            'WMI_EXPIRED_DATE': '2016-05-21 11:34:34',
            'WMI_CREATE_DATE': '2016-04-21 11:34:34',
            'WMI_UPDATE_DATE': '2016-04-21 11:34:34',
            'WMI_ORDER_STATE': 'Created',
            'extra_data': json.dumps({'EXTRA': 'Value'})
        }
        self.payment = WalletOneSuccessPayment.objects.create(**self.data)

    def test_model_can_get_extra_attr(self):
        payment = WalletOneSuccessPayment.objects.get(
            WMI_ORDER_ID='336077917075'
        )
        self.assertEqual(payment.extra_attrs.EXTRA, 'Value')

    def test_payment_attribute_proxy(self):
        proxy = PaymentAttributeProxy(self.payment)
        self.assertEqual(proxy._get_data(), {'EXTRA': 'Value'})
        self.assertEqual(proxy.EXTRA, 'Value')
        proxy.EXTRA1 = 'Value1'
        self.assertEqual(
            proxy._get_data(), {'EXTRA': 'Value', 'EXTRA1': 'Value1'}
        )