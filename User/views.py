from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import User
from .forms import RegistrationForm, SignUpForm


# Create your views here.



class RegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url


class ProfileView(UpdateView):
    model = User
    fields = "__all__"
    template_name = 'registration/profile.html'

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        return self.request.user

from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm

class Signup(SuccessMessageMixin, CreateView):
    form = UserCreationForm
    fields = '__all__'
    model = User
    template_name = 'registration/signup.html'
    # success_url = reverse_lazy('glazes:home page')


def signUp(req):
    if req.method == "POST":
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            auth_login(req, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = SignUpForm()

    context = {
        "form": form,
    }

    return render(req, "registration/signUp.html", context=context)



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.