from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from vipcontacts import views
from vipcontacts.reusing import views_login

router = routers.DefaultRouter()
router.register(r'person', views.PersonViewSet)
router.register(r'alias', views.AliasViewSet)
router.register(r'address', views.AddressViewSet)
router.register(r'relationship', views.RelationShipViewSet)
router.register(r'phone', views.PhoneViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'job', views.JobViewSet)
router.register(r'mail', views.MailViewSet)
router.register(r'log', views.LogViewSet)
router.register(r'search', views.SearchViewSet)
router.register(r'blob', views.BlobViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', views_login.login), 
    path('logout/', views_login.logout), 
    path('api/blobnames/', views.blob_names),
    path('api/professions/', views.professions),
    path('api/organizations/', views.organizations),
    path('api/departments/', views.departments),
    path('api/groups/', views.groups),
    path('api/groups/deletebyname/', views.delete_group_by_name),
    path('api/groups/members/', views.group_members),
    path('api/groups/members/full/', views.group_members_full),
    path('api/titles/', views.titles),
    path('api/statistics/', views.statistics),
    path('api/merge_text_fields/<str:table>/<str:field>/', views.merge_text_fields),
    path('persons/merge/', views.PersonsMerge), 
    path('next_important_dates/', views.NextImportantDates), 
    
    
    
    
    
    
]

