from django.conf.urls import url, include


urlpatterns = [
    url(r'^w1/', include('walletone.urls')),
]
