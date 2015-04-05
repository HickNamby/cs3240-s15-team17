from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SecureWitness.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^submit/', 'SecureWitness.views.submit'),
    url(r'^index/', 'SecureWitness.views.index'),
    url(r'^submitted/', 'SecureWitness.views.submitted'),
	url(r'^report/(?P<report_id>\d+)', 'SecureWitness.views.report_view'),
    url(r'^list', 'SecureWitness.views.list'),
    url(r'^', 'SecureWitness.views.home'),


)
