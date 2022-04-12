from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, DeleteView

from cookbook.accounts.forms import ProfileCreationForm, ProfileLoginForm, EditProfileForm
from cookbook.common.helpers import RedirectLoggedUsersToDashboardMixin
from cookbook.accounts.models import Profile, CbUser


class UserRegisterView(RedirectLoggedUsersToDashboardMixin, CreateView):
    form_class = ProfileCreationForm
    template_name = 'accounts/register2.html'
    success_url = reverse_lazy('dashboard', kwargs={'category': 'all'})

    def form_valid(self, form):
        valid = super().form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        auth_user = authenticate(email=email, password=password)
        login(self.request, auth_user)
        return valid


class UserLoginView(RedirectLoggedUsersToDashboardMixin, LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard', kwargs={'category': 'all'})
    form_class = ProfileLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(LogoutView):
    next_page = 'login'


class ProfileEditView(AccessMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/edit-profile.html'

    context_object_name = 'profile'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user != self.object.user:
            return redirect('403')
        return response


class ProfileDeleteView(AccessMixin, DeleteView):
    model = CbUser
    template_name = 'accounts/profile-delete.html'
    fields = ()
    success_url = reverse_lazy('home')
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        user_object = self.get_object()
        response = super().dispatch(request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user != user_object:
            return redirect('403')
        return response


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = self.object.user.recipe_set.all
        context['recipes'] = recipes
        context['is_owner'] = self.object.user == self.request.user
        return context


class UnauthorizedView(TemplateView):
    template_name = 'base/403.html'
