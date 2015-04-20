from django.conf.urls import patterns, include, url
from django.contrib import admin

from admin import user_admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SecureWitness.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^submit/', 'SecureWitness.views.submit'),
    url(r'^index/', 'SecureWitness.views.index'),
    url(r'^submitted/', 'SecureWitness.views.submitted'),
	url(r'^report/(?P<report_id>\d+)(?:/(?P<file_id>\d+))?/?$', 'SecureWitness.views.report_view'),
    url(r'^folder/(?P<folder_id>\d+)/$', 'SecureWitness.views.folder_view'),
    url(r'^profile', 'SecureWitness.views.profile'),
    url(r'^createfolder', 'SecureWitness.views.createfolder'),
    url(r'^editfolder/(?P<folder_id>\d+)/$', 'SecureWitness.views.editfolder'),
    url(r'^editreport/(?P<report_id>\d+)/$', 'SecureWitness.views.editreport'),
    url(r'^register/$', 'SecureWitness.views.register'),
    url(r'^login/$', 'SecureWitness.views.user_login'),
    url(r'^useradmin/',include(user_admin.urls)),
    url(r'^creategroup/$','SecureWitness.views.create_group'),
    url(r'^', 'SecureWitness.views.home'),
)
