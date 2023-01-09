
from django.contrib import admin
from django.urls import path, include

from core.views import user_list, login_v2
admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', user_list, name="user-list"),
    path('login/', login_v2, name="login-v2"),
]
