from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from website import views

urlpatterns = [
    path('', RedirectView.as_view(url='/zh/', permanent=False)),
    path('admin/', admin.site.urls),
    path('health/', views.health, name='health'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
]
urlpatterns += i18n_patterns(path('', include('website.urls')))
