from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from vipcontacts import views

router = routers.DefaultRouter()
router.register(r'api/persons', views.PersonViewSet)
router.register(r'api/alias', views.AliasViewSet)
router.register(r'api/address', views.AddressViewSet)
router.register(r'api/relationship', views.RelationShipViewSet)
router.register(r'api/phone', views.PhoneViewSet)
router.register(r'api/mail', views.MailViewSet)
router.register(r'api/log', views.LogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', views.login), 
    path('logout/', views.logout), 
    path('api/persons/search/<slug:search>/', views.person_search),
]

