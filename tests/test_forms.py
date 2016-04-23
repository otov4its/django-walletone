# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.test import SimpleTestCase, TestCase

from walletone.forms import WalletOnePaymentForm, WalletOneConfirmForm
from walletone.models import WalletOneSuccessPayment
from walletone import settings

from .utils import override_settings


class PaymentFormTestCase(SimpleTestCase):
    def test_payment_form_contains_default_fields(self):
        form = WalletOnePaymentForm()
        default_fields = [
            'WMI_MERCHANT_ID',
            'WMI_PAYMENT_AMOUNT',
            'WMI_CURRENCY_ID',
            'WMI_DESCRIPTION',
            'WMI_SUCCESS_URL',
            'WMI_FAIL_URL',
        ]
        for field_name in default_fields:
            self.assertIn(field_name, form.as_p())

    def test_payment_form_contains_extra_fields(self):
        extra_fields = {
            'EXTRA1': 'value1',
            'EXTRA2': 'value2',
        }
        form = WalletOnePaymentForm(initial=extra_fields)
        for field_name in extra_fields.keys():
            self.assertIn(field_name, form.as_p())

    def test_payment_form_contains_signature_field_if_any(self):
        with override_settings(SIGN_METHOD=None):
            form = WalletOnePaymentForm()
            self.assertNotIn('WMI_SIGNATURE', form.as_p())

        with override_settings(SIGN_METHOD='md5'):
            form = WalletOnePaymentForm()
            self.assertIn('WMI_SIGNATURE', form.as_p())

        with override_settings(SIGN_METHOD='sha1'):
            form = WalletOnePaymentForm()
            self.assertIn('WMI_SIGNATURE', form.as_p())

    def test_payment_form_contains_correct_action_url(self):
        form = WalletOnePaymentForm()
        self.assertEqual(form.action_url, settings.FORM_ACTION_URL)

    def test_payment_form_get_correct_signature_string(self):
        fields = {
            'WMI_MERCHANT_ID': '000000000000',
            'WMI_PAYMENT_AMOUNT': '99.99',
            'WMI_CURRENCY_ID': '643',
            'WMI_DESCRIPTION': 'Описание',
            'WMI_SUCCESS_URL': '',
            'WMI_FAIL_URL': '',
            'EXTRA_FIELD': 'Привет Мир!'
        }
        form = WalletOnePaymentForm(initial=fields)
        correct_signature_string = 'Привет Мир!643Описание00000000000099.99'
        correct_signature_string += settings.SECRET_KEY
        self.assertEqual(form._get_signature_string(), correct_signature_string)

    def test_payment_form_get_correct_signature(self):
        fields = {
            'WMI_MERCHANT_ID': '000000000000',
            'WMI_PAYMENT_AMOUNT': '99.99',
            'WMI_CURRENCY_ID': '643',
            'WMI_DESCRIPTION': 'Описание',
            'WMI_SUCCESS_URL': '',
            'WMI_FAIL_URL': '',
            'EXTRA_FIELD': 'Привет Мир!'
        }
        form = WalletOnePaymentForm(initial=fields)
        correct_signature = b'ATQEIrh2C7jXGDzj/fJ4JQ=='
        self.assertEqual(form._get_signature(), correct_signature)

        with override_settings(SIGN_METHOD=None):
            form = WalletOnePaymentForm(initial=fields)
            self.assertEqual(form._get_signature(), '')


class ConfirmFormTestCase(TestCase):
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
            # howerer its present in form data
            'WMI_AUTO_ACCEPT': '1',
            'WMI_NOTIFY_COUNT': '0',
        }
        self.form = WalletOneConfirmForm(self.data)

    def test_confirm_form_contains_extra_fields(self):
        self.assertIn('EXTRA_FIELD', self.form.as_p())

    def test_confirm_form_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_confirm_form_is_not_valid_if_wrong_signature(self):
        self.data['WMI_SIGNATURE'] = 'bad'
        self.assertFalse(WalletOneConfirmForm(self.data).is_valid())

    def test_confirm_form_cleaned_data_contains_extra_data_json(self):
        if self.form.is_valid():
            self.assertEqual(
                self.form.cleaned_data['extra_data'],
                json.dumps({'EXTRA_FIELD': 'value'})
            )

    def test_confirm_form_saves_payment_to_db(self):
        if self.form.is_valid():
            payment = self.form.save()
            db_payment = WalletOneSuccessPayment.objects.get(
                WMI_ORDER_ID=payment.WMI_ORDER_ID
            )
            self.assertEqual(payment, db_payment)

    def test_if_saved_payment_can_get_extra_attrs(self):
        if self.form.is_valid():
            payment = self.form.save()
            self.assertEqual(
                payment.extra_attrs.EXTRA_FIELD,
                self.data['EXTRA_FIELD']
            )