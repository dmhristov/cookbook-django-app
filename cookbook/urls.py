from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from cookbook.main.views import HomePageView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomePageView.as_view(), name='home'),
                  path('profile/', include('cookbook.accounts.urls')),
                  path('recipes/', include('cookbook.main.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
