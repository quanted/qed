from django.conf import settings
from django.conf.urls import include, url
# from django.urls import path
import login_middleware
from django.contrib.auth.decorators import login_required
import os

#regular expressions
# the r in r'^cts/index.html$' indicates that what is inside the quotes is a regular expression
# the ^ in r'^cts/index.html$' indicates that we are looking to extend from the root dir from this part of the string
# the $ in r'^cts/index.html$' indicates that we are looking to extend end the mathing part exactly here

print('qed.urls')
print("IS_PUBLIC: " + str(os.environ.get('IS_PUBLIC')))

#appends to the list of url patterns to check against
# if settings.IS_PUBLIC:
# if _is_public:
# Storing env vars in os.environ are strings only...
if os.environ.get('IS_PUBLIC') == "True":
    urlpatterns = [
        # url(r'^login/auth/?$', login_middleware.login_auth),
        # url(r'^login*', login_middleware.login),
        url(r'^$', include('splash_app.urls'), name='home'),
        url(r'^login/?$', login_middleware.login),
        url(r'^cts/', include('cts_app.urls')),
        url(r'^cyan/', include('cyan_app.urls')),
        url(r'^ubertool/', include('ubertool_app.urls')),
    ]
else:
    urlpatterns = [
        url(r'^', include('splash_app.urls')),
        # url(r'^login/?$', login_middleware.login),
        url(r'^cts/', include('cts_app.urls')),
        url(r'^cyan/', include('cyan_app.urls')),
        #url(r'^hem/', include('hem_app.urls')),
        url(r'^hms/', include('hms_app.urls')),
        url(r'^hwbi/', include('hwbi_app.urls')),
        url(r'^pisces/', include('pisces_app.urls')),
        url(r'^ubertool/', include('ubertool_app.urls')),

        # path('', include('splash_app.urls')),
        # path('cts/', include('cts_app.urls')),
        # path('cyan/', include('cyan_app.urls')),
        # path('hms/', include('hms_app.urls')),
        # path('hwbi/', include('hwbi_app.urls')),
        # path('pisces/', include('pisces_app.urls')),
        # path('ubertool/', include('ubertool_app.urls')),
    ]

if settings.IS_PUBLIC:
    # 404 Error view (file not found)
    handler404 = 'splash_app.views.file_not_found'
    # 500 Error view (server error)
    handler500 = 'splash_app.views.file_not_found'
    # 403 Error view (forbidden)
    handler403 = 'splash_app.views.file_not_found'
else: # the same for now
    # 404 Error view (file not found)
    handler404 = 'splash_app.views.file_not_found'
    # 500 Error view (server error)
    handler500 = 'splash_app.views.file_not_found'
    # 403 Error view (forbidden)
    handler403 = 'splash_app.views.file_not_found'
