from django.conf import settings
from django.conf.urls import include, url
from django.urls import path, re_path
from splash_app.views import landing
import login_middleware
from django.contrib.auth.decorators import login_required
import os

print('qed.urls')
print("IS_PUBLIC: " + str(os.environ.get('IS_PUBLIC')))

# Storing env vars in os.environ are strings only...
# if bool(os.environ.get('IS_PUBLIC')) and not bool(os.environ.get('UNDER_REVIEW')):
if os.environ.get('IS_PUBLIC') == "True":
    urlpatterns = [
        path('', include('splash_app.urls')),
        path('cts/', include('cts_app.urls')),
        # path('cyan/', include('cyan_app.urls')),
        path('login/', login_middleware.login),
        # path('pisces/', include('pisces_app.urls')),
        path('pram/', include('pram_app.urls')),
        path('nta/', include('nta_app.urls')),
        path('hms/', include('hms_app.urls'))
        # path('ubertool/', include('ubertool_app.urls')),
        # re_path(r'^(?s).*', landing.page_404)
    ]
else:
    # not public, no password protection (dev, staging, etc.)
    urlpatterns = [
        path('', include('splash_app.urls')),
        path('cts/', include('cts_app.urls')),
        path('cyan/', include('cyan_app.urls')),
        path('hms/', include('hms_app.urls')),
        # path('hem/', include('hem_app.urls')),
        path('hwbi/', include('hwbi_app.urls')),
        path('pisces/', include('pisces_app.urls')),
        path('pram/', include('pram_app.urls')),
        path('nta/', include('nta_app.urls'))
    ]

if settings.IS_PUBLIC:
    # 404 Error view (file not found)
    handler404 = 'splash_app.views.landing.page_404'
    # 500 Error view (server error)
    handler500 = 'splash_app.views.landing.page_404'
    # 403 Error view (forbidden)
    handler403 = 'splash_app.views.landing.page_404'
else: # the same for now
    # 404 Error view (file not found)
    handler404 = 'splash_app.views.landing.page_404'
    # 500 Error view (server error)
    handler500 = 'splash_app.views.landing.page_404'
    # 403 Error view (forbidden)
    handler403 = 'splash_app.views.landing.page_404'
