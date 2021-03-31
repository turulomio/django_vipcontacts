from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from vipcontacts import views

router = routers.DefaultRouter()
router.register(r'api/persons', views.PersonViewSet)
router.register(r'api/alias', views.AliasViewSet)
router.register(r'api/address', views.AddressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', views.login), 
    path('logout/', views.logout), 
#    path('api/persons/<int:pk>', views.PersonViewSet.as_view({'get':'retrieve'})),
    
]

