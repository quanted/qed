from django.conf import settings
from django.conf.urls import include, url

#regular expressions
# the r in r'^cts/index.html$' indicates that what is inside the quotes is a regular expression
# the ^ in r'^cts/index.html$' indicates that we are looking to extend from the root dir from this part of the string
# the $ in r'^cts/index.html$' indicates that we are looking to extend end the mathing part exactly here

print('qed.urls')
#appends to the list of url patterns to check against
if settings.IS_PUBLIC:
    urlpatterns = [
        url(r'^$', include('splash_app.urls'),name='home'),
    ]
else:
    urlpatterns = [
        url(r'^', include('splash_app.urls')),
        #url(r'^admin/', include('admin.site.urls')),
        url(r'^cts/', include('cts_app.urls')),
        url(r'^cyan/', include('cyan_app.urls')),
        #url(r'^hem/', include('hem_app.urls')),
        url(r'^hms/', include('hms_app.urls')),
        url(r'^hwbi/', include('hwbi_app.urls')),
        url(r'^pisces/', include('pisces_app.urls')),
        url(r'^pop/', include('pop_app.urls')),
        url(r'^sam/', include('sam_app.urls')),
        url(r'^ubertool/', include('ubertool_app.urls')),
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
