from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'TFG.views.home', name='home'),
    #url(r'^TFG/', include('TFG.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #Home
    url(r'^$', 'principal.views.main_view', name='Inicio'),

    #Select thread
    url(r'^selected_thread/(?P<id>\d+)/$', 'principal.views.analyze_thread', name="selected_thread"),

    #Results_list
    url(r'^last-results/', 'principal.views.results_list', name='last-results'),

    #Select old result
    url(r'^selected_result/(?P<id>\d+)/$', 'principal.views.view_result', name="selected_result"),

    #Remove one result
    url(r'^remove_result/(?P<id>\d+)/$', 'principal.views.remove_one_result', name="remove_result"),

    #Drop collection results
    url(r'^drop-results/', 'principal.views.drop_results', name='drop-results'),
)
