from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from vipcontacts import views

router = routers.DefaultRouter()
router.register(r'api/persons', views.PersonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    path('login/', views.login), 
    path('logout/', views.logout), 
]

