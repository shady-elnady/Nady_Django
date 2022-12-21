"""Config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

import debug_toolbar


urlpatterns = [
    path('account/', include('Account.urls')), # allauth 3rd Library
    path("", include("django.contrib.auth.urls")), # Default Auth URL
    path('accounts/', include('allauth.urls')), # allauth 3rd Library
    path("", include("Laboratory.urls", namespace="Laboratory")),
    path("", include("GraphQL.urls", namespace= "GraphQL")),
    path("digit/", include("Digit.urls", namespace="Digit")),
    path("payment", include("Payment.urls", namespace= "Payment")),
    path('admin/', admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path('Entities', include('django_spaghetti.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
