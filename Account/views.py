from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.views.generic import TemplateView


# Create your views here.



class SplashView(TemplateView):
    template_name = "Splash/index.html"


## from Velzon

class MyPasswordChangeView( PasswordChangeView):
    success_url = reverse_lazy("dashboards:dashboard")


class MyPasswordSetView( PasswordSetView):
    success_url = reverse_lazy("dashboards:dashboard")