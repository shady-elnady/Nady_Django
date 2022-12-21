from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.views.generic import TemplateView


# Create your views here.



class SplashView(TemplateView):
    template_name = "Splash/index.html"
    # context_object_name = 'splash_word'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(SplashView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['splash_word'] = [
            *'Welcome',
            ': )',
        ]
        context['bg_colors'] = [
            "#eb4747",
            "#ebc247",
            "#99eb47",
            "#47eb70",
            "#47ebeb",
            "#4770eb",
            "#9947eb",
            "#eb47c2",
            "#eb4747",
        ]
        return context
    


## from Velzon

class MyPasswordChangeView( PasswordChangeView):
    success_url = reverse_lazy("dashboards:dashboard")


class MyPasswordSetView( PasswordSetView):
    success_url = reverse_lazy("dashboards:dashboard")