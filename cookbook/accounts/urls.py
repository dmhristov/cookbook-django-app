from django.urls import path

from cookbook.accounts.views import UserRegisterView, UserLoginView, ProfileEditView, UserLogoutView, \
    ProfileDetailsView, UnauthorizedView, ProfileDeleteView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit/<int:pk>/', ProfileEditView.as_view(), name='edit profile'),
    path('delete/<int:pk>/', ProfileDeleteView.as_view(), name='delete profile'),
    path('unauthorized/', UnauthorizedView.as_view(), name='403')
]
