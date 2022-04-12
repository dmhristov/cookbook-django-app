from django.urls import path

from cookbook.main.views import DashboardView, CreateRecipeView, RecipeDetailsView, CreateCommentView, \
    CreateCommenReplytView, EditRecipeView, DeleteRecipeView, likes_view

urlpatterns = [
    path('dashboard/<str:category>/', DashboardView.as_view(), name='dashboard'),
    path('create/', CreateRecipeView.as_view(), name='create recipe'),
    path('details/<int:pk>/', RecipeDetailsView.as_view(), name='recipe details'),
    path('details/<int:pk>/like/', likes_view, name='likes'),
    path('edit/<int:pk>/', EditRecipeView.as_view(), name='edit recipe'),
    path('delete/<int:pk>/', DeleteRecipeView.as_view(), name='delete recipe'),
    path('details/<int:pk>/comments', CreateCommentView.as_view(), name='comments'),
    path('details/<int:pk>/comments/<int:comment_pk>/replies/', CreateCommenReplytView.as_view(),
         name='replies'),
]
