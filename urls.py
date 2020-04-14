from django.conf import settings
from django.conf.urls import include, url
from django.urls import path, re_path
from splash_app.views import landing
import importlib
import login_middleware
from django.contrib.auth.decorators import login_required
import os

print('qed.urls')
print("IS_PUBLIC: " + str(os.environ.get('IS_PUBLIC')))

# Workaround import of cyano urls due to dashes in repo name:
cyano = importlib.import_module(".urls", "EPA-Cyano-Web.cyan_django")
cyano_urls = getattr(cyano, 'urlpatterns')

# Storing env vars in os.environ are strings only...
# if bool(os.environ.get('IS_PUBLIC')) and not bool(os.environ.get('UNDER_REVIEW')):
if os.environ.get('IS_PUBLIC') == "True":
    urlpatterns = [
        path('', include('splash_app.urls')),
        path('cts/', include('cts_app.urls')),
        # path('cyan/', include('cyan_app.urls')),
        path('hms/', include('hms_app.urls')),
        # path('hwbi/', include('hwbi_app.urls')),
        path('login/', login_middleware.login),
        path('nta/', include('nta_app.urls')),
        path('pisces/', include('pisces_app.urls')),
        path('pram/', include('pram_app.urls')),
        path('cyanweb/', include(cyano_urls)),
    ]
else:
    # not public (dev, staging, etc.)
    urlpatterns = [
        path('', include('splash_app.urls')),
        path('cts/', include('cts_app.urls')),
        path('cyan/', include('cyan_app.urls')),
        path('hms/', include('hms_app.urls')),
        path('hwbi/', include('hwbi_app.urls')),
        path('nta/', include('nta_app.urls')),
        path('pisces/', include('pisces_app.urls')),
        path('pram/', include('pram_app.urls')),
        path('login/', login_middleware.login),
        path('cyanweb/', include(cyano_urls)),
    ]

# 404 Error view (file not found)
handler404 = 'splash_app.views.landing.page_404'
# 500 Error view (server error)
handler500 = 'splash_app.views.landing.page_404'
# 403 Error view (forbidden)
handler403 = 'splash_app.views.landing.page_404'
