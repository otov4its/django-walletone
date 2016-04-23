from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^confirm/$', views.payment_confirm, name='w1-payment-confirm'),
]