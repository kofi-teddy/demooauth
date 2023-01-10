
from django.contrib import admin
from django.urls import include, path

from core.views import login_v2, revoke_token_hjjh, user_list

admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', user_list, name="user-list"),
    path('login/', login_v2, name="login-v2"),
    path('logout/', revoke_token_hjjh, name="login-v2"),
]
