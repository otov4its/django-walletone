# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import json
from base64 import b64encode

from django import forms

from . import settings as w1_settings
from .models import WalletOneSuccessPayment


class SignatureMixin(object):
    def _val(self, name):
        # When form was received
        if self.is_bound:
            val = self.data.get(name)
        # When form prepares for sending
        else:
            val = self.initial.get(name, self.fields[name].initial)

        return val if val else ''

    def _get_signature(self):
        if not w1_settings.SIGN_METHOD:
            return ''
        hash_func = getattr(hashlib, w1_settings.SIGN_METHOD)
        hash_string = hash_func(self._get_signature_string()
                                .encode('1251')).digest()
        return b64encode(hash_string)

    def _get_signature_string(self):
        fields = self.data if self.is_bound else self.fields
        signature_string = ''
        for name in sorted(fields.keys(), key=lambda s: s.lower()):
            if name == 'WMI_SIGNATURE':
                continue
            signature_string += self._val(name)
        signature_string += w1_settings.SECRET_KEY

        return signature_string


class WalletOnePaymentForm(SignatureMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super(WalletOnePaymentForm, self).__init__(*args, **kwargs)

        # Creating mandatory form fields
        self.fields['WMI_MERCHANT_ID'] = forms.CharField(
            initial=w1_settings.MERCHANT_ID
        )
        self.fields['WMI_PAYMENT_AMOUNT'] = forms.CharField(
            initial='0.00'
        )
        self.fields['WMI_CURRENCY_ID'] = forms.CharField(
            initial=w1_settings.CURRENCY_DEFAULT
        )
        self.fields['WMI_DESCRIPTION'] = forms.CharField(
            initial='Описание'
        )
        self.fields['WMI_SUCCESS_URL'] = forms.CharField(
            initial=w1_settings.SUCCESS_URL
        )
        self.fields['WMI_FAIL_URL'] = forms.CharField(
            initial=w1_settings.FAIL_URL
        )

        # Creating other form fields
        if 'initial' in kwargs:
            for name, value in kwargs['initial'].items():
                self.fields[name] = forms.CharField(initial=value)

        # Creating WMI_SIGNATURE field and calculates signature if any
        if w1_settings.SIGN_METHOD:
            self.fields['WMI_SIGNATURE'] = forms.CharField(
                max_length=24, initial=self._get_signature())

        # HiddenInput widget as default
        # required=False as default
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()
            self.fields[field].required = False

        # For using as form action url in templates, e.g.
        # <form method="post" action="{{ form.action_url }}">
        self.action_url = w1_settings.FORM_ACTION_URL


class WalletOneConfirmForm(SignatureMixin, forms.ModelForm):
    class Meta:
        model = WalletOneSuccessPayment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WalletOneConfirmForm, self).__init__(*args, **kwargs)

        # Creating extra form fields
        for name in self.data.keys():
            if not name.startswith('WMI_'):
                self.fields[name] = forms.CharField(initial='', required=False)

    def clean(self):
        cleaned_data = super(WalletOneConfirmForm, self).clean()
        # When form was received
        if self.is_bound:
            if w1_settings.SIGN_METHOD:
                signature = self.data.get('WMI_SIGNATURE').encode('1251')
                if signature != self._get_signature():
                    raise forms.ValidationError('WMI_SIGNATURE error')
        # Pack extra fields into extra_data form field
        cleaned_data['extra_data'] = json.dumps(
            {key: value for key, value in cleaned_data.items()
             if not key.startswith('WMI_') and key != 'extra_data'}
        )
        return cleaned_data
