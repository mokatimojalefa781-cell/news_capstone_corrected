from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('news.api_urls')),
    path('api-auth/', include('rest_framework.urls')),

    # direct login/logout without /accounts/ prefix
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
