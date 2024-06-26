"""
URL configuration for Pikt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from Authentication import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from invoicing import views as invoicing_views
from ebay import views as ebay_views

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('sentry-debug/', trigger_error),
    path('admin/', admin.site.urls),
    path('', views.homeView.as_view()),
    path('login/', views.loginView.as_view(), name='login'),
    path('register/', views.registerView.as_view(), name='register'),
    path('account/', views.accountView.as_view(), name='account'),
    path('dashboards/', include('dashboards.urls')),
    path('company/', include('company.urls')),
    path('account/upload_avatar/', views.uploadAvatarView.as_view(), name='upload_avatar'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboards/generate-quote/<int:customer_id>/', invoicing_views.generate_quote, name='generate_quote'),
    path('send-invoice/<int:invoice_id>/', invoicing_views.send_invoice, name='send_invoice'),
    path('save-ebay-policies/', ebay_views.SaveEbayPoliciesView.as_view(), name='save_ebay_policies'),
    path('set-parts-ebay-listed/', ebay_views.SetPartsEbayListedView.as_view(), name='mark_as_ebay_listed'),
    path('ebay-data-feed', ebay_views.EbayDataFeedView.as_view(), name='ebay_data_feed'),
    path('ebay_consent/redirect/', views.RedirectView.as_view(), name='redirect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

