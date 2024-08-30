from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from login_auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/',auth_views.signup, name='signup'),


]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)