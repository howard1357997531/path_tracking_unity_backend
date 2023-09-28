from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'get_object_3d', views.get_object_3d, basename='get_object_3d')

urlpatterns = [
    path('', include(router.urls)),
    path('Generate_3D_object/', views.Generate_3D_object.as_view(), name="Generate_3D_object"),
    path('test/', views.test.as_view(), name="test"),
    path('Detail_3D_object/<int:pk>/', views.Detail_3D_object.as_view(), name="Detail_3D_object"),
    path('ChangeSelect_3DObject/<int:pk>/', views.ChangeSelect_3DObject.as_view(), name="ChangeSelect_3DObject"),
    path('SavePly/', views.SavePly.as_view(), name="SavePly")
]
