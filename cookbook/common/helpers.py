from django.shortcuts import redirect
from django.urls import reverse_lazy


class AddBootstrapFormCLassMixin:
    fields = {}

    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form-control form-control-lg'


class RedirectLoggedUsersToDashboardMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard', 'all')
        return super().dispatch(request, *args, **kwargs)


class InvalidCommentRedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not args:
            return redirect(reverse_lazy('recipe details', kwargs={'pk': kwargs['pk']}))
        return response
