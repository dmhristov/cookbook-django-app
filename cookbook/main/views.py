from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, DeleteView

from cookbook.main.forms import CreateRecipeForm, CreateCommentForm, CreateCommentReplyForm, EditRecipeForm
from cookbook.common.helpers import RedirectLoggedUsersToDashboardMixin
from cookbook.main.models import Recipe, Comment, Reply, Like
from cookbook.accounts.models import Profile


class HomePageView(RedirectLoggedUsersToDashboardMixin, TemplateView):
    template_name = 'main/home-no-profile.html'


class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'main/dashboard.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        if self.kwargs['category'] != "all":
            return Recipe.objects.filter(category=self.kwargs['category'])
        return Recipe.objects.all()


class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'main/create-recipe.html'
    success_url = reverse_lazy('dashboard', kwargs={'category': 'all'})
    form_class = CreateRecipeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditRecipeView(AccessMixin, UpdateView):
    model = Recipe
    template_name = 'main/edit-recipe.html'
    form_class = EditRecipeForm
    context_object_name = 'recipe'

    def get_success_url(self):
        return reverse_lazy('recipe details', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user != self.object.author:
            return redirect('403')
        return response


class DeleteRecipeView(AccessMixin, DeleteView):
    model = Recipe
    template_name = 'main/delete-recipe.html'
    context_object_name = 'recipe'
    fields = ()
    success_url = reverse_lazy('dashboard', kwargs={'category': 'all'})

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        if self.request.user != self.object.author:
            return redirect('403')
        return response


class RecipeDetailsView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'main/recipe-details.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.object.author_id)
        context['is_owner'] = self.object.author == self.request.user
        context['comment_form'] = CreateCommentForm
        context['reply_form'] = CreateCommentReplyForm
        context['comments'] = Comment.objects.filter(recipe_id=self.object.id)
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'main/recipe-details.html'
    form_class = CreateCommentForm

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not self.args:
            return redirect(reverse_lazy('recipe details', kwargs={'pk': self.kwargs['pk']}))
        return response

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.recipe_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe details', kwargs={'pk': self.kwargs['pk']})


class CreateCommenReplytView(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'main/recipe-details.html'
    form_class = CreateCommentReplyForm

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not self.args:
            return redirect(reverse_lazy('recipe details', kwargs={'pk': self.kwargs['pk']}))
        return response

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.comment_id = self.kwargs['comment_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe details', kwargs={'pk': self.kwargs['pk']})


@login_required
def likes_view(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    user = request.user

    new_like, created = Like.objects.get_or_create(user=user, recipe=recipe)

    if created:
        recipe.total_likes += 1
        recipe.save()
    return redirect('recipe details', pk)
