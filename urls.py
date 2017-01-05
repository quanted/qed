from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', include('splash_app.urls')),
    #url(r'^cts/', include('cts_app.urls')),
    #url(r'^cyan/', include('cyan_app.urls')),
    #url(r'^hem/', include('hem_app.urls')),
    #url(r'^hms/', include('hms_app.urls')),
    #url(r'^hwbi/', include('hwbi_app.urls')),
    #url(r'^pisces/', include('pisces_app.urls')),
    #url(r'^pop/', include('pop_app.urls')),
    #url(r'^ubertool/', include('ubertool_app.urls')),
]