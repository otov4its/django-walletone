# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .forms import WalletOneConfirmForm
from . import signals


logger = logging.getLogger(__name__)


@csrf_exempt
def payment_confirm(request):
    if request.method == 'POST':
        logger.info('Received a request from WalletOne')
        confirm_form = WalletOneConfirmForm(request.POST)
        if confirm_form.is_valid():
            payment = confirm_form.save()
            logger.info('Payment was created')
            # Send signal with payment object as arguments
            signals.payment_received.send(sender=type(payment), payment=payment)
            logger.info('payment_received signal was sent')
            return HttpResponse('WMI_RESULT=OK')
        else:
            errors_message = ''
            for key, messages in confirm_form.errors.items():
                errors_message += ' '.join(messages)
            errors_message = 'Received form not valid: ' + errors_message
            logger.warning(errors_message)
            return HttpResponse(
                'WMI_RESULT=OK&WMI_DESCRIPTION=%s' % errors_message
            )
    else:
        return HttpResponseBadRequest("Expected POST request")