# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from walletone.models import WalletOneSuccessPayment
from walletone.signals import payment_received


class PaymentConfirmViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'WMI_MERCHANT_ID': '165531803223',
            'WMI_PAYMENT_AMOUNT': '1.00',
            'WMI_COMMISSION_AMOUNT': '0.00',
            'WMI_CURRENCY_ID': '643',
            'WMI_PAYMENT_NO': '1',
            'WMI_ORDER_ID': '336077917075',
            'WMI_DESCRIPTION': 'Мой тестовый заказ',
            'WMI_EXPIRED_DATE': '2016-05-21 11:34:34',
            'WMI_CREATE_DATE': '2016-04-21 11:34:34',
            'WMI_UPDATE_DATE': '2016-04-21 11:34:34',
            'WMI_ORDER_STATE': 'Created',
            'WMI_SIGNATURE': 'Q0vBjbeAaoFKTVcjUfkKLw==',
            'EXTRA_FIELD': 'value',
            # Not documented fields
            # howerer its may present in form data
            'WMI_AUTO_ACCEPT': '1',
            'WMI_NOTIFY_COUNT': '0',
        }

        self.confirm_url = reverse('w1-payment-confirm')

    def test_view_returns_400_if_get_request(self):
        response = self.client.get(self.confirm_url)
        self.assertEqual(response.status_code, 400)

    def test_view_returns_200_if_post_request(self):
        response = self.client.post(self.confirm_url, self.data)
        self.assertContains(response, 'WMI_RESULT=OK')

    def test_view_saves_payment_to_db(self):
        self.client.post(self.confirm_url, self.data)
        try:
            WalletOneSuccessPayment.objects.get(WMI_ORDER_ID='336077917075')
        except WalletOneSuccessPayment.DoesNotExist:
            self.fail("payment DoesNotExist")
        except WalletOneSuccessPayment.MultipleObjectsReturned:
            self.fail("payment MultipleObjectsReturned")

    def test_view_sends_a_signal(self):
        def receiver(**kwargs):
            receiver.signal_was_sent = True
            payment = kwargs['payment']
            self.assertEqual(
                payment,
                WalletOneSuccessPayment.objects.get(
                    WMI_ORDER_ID=payment.WMI_ORDER_ID
                )
            )
        receiver.signal_was_sent = False
        payment_received.connect(receiver, sender=WalletOneSuccessPayment)
        self.client.post(self.confirm_url, self.data)
        self.assertTrue(receiver.signal_was_sent)

    def test_view_was_called_twice_with_same_wmi_order_id(self):
        response1 = self.client.post(self.confirm_url, self.data)
        self.assertEqual(response1.content, b'WMI_RESULT=OK')
        response2 = self.client.post(self.confirm_url, self.data)
        self.assertContains(response2, 'not valid')

    def test_view_with_bad_signature(self):
        self.data['WMI_SIGNATURE'] = 'bad'
        response = self.client.post(self.confirm_url, self.data)
        self.assertContains(response, 'not valid')
