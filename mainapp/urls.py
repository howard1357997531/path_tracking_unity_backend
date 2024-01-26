from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'get_object_3d', views.get_object_3d, basename='get_object_3d')

urlpatterns = [
    path('', include(router.urls)),
    path('save_draw_object/', views.save_draw_object, name="save_draw_object"),
    path('get_draw_object/', views.get_draw_object, name="get_draw_object"),
    path('edit_draw_object_order/', views.edit_draw_object_order, name="edit_draw_object_order"),
    path('get_single_draw_object/<int:pk>/', views.get_single_draw_object, name="get_single_draw_object"),
    path('pin_draw_object/<int:pk>/', views.pin_draw_object, name="pin_draw_object"),
    path('select_draw_object/<int:pk>/', views.select_draw_object, name="select_draw_object"),
    path('execute_robot/', views.execute_robot, name="execute_robot"),
    path('open_camera/', views.open_camera, name="open_camera"),
    path('screen_shot/', views.screen_shot, name="screen_shot"),
    path('save_ply/', views.save_ply, name="save_ply"),
    path('preprocessing_ply/', views.preprocessing_ply, name="preprocessing_ply"),
    path('get_initial_object/', views.get_initial_object, name="get_initial_object"),
    path('pin_initial_object/<int:pk>/', views.pin_initial_object, name="pin_initial_object"),
    path('select_initial_object/<int:pk>/', views.select_initial_object, name="select_initial_object"),
    path('initial_3D_object/', views.initial_3D_object.as_view(), name="initial_3D_object"),
    path('initial_3D_object_detail/<int:pk>/', views.initial_3D_object_detail.as_view(), name="initial_3D_object_detail"),
    path('Generate_3D_object/', views.Generate_3D_object.as_view(), name="Generate_3D_object"),
    path('test/', views.test.as_view(), name="test"),
    path('Detail_3D_object/<int:pk>/', views.Detail_3D_object.as_view(), name="Detail_3D_object"),
    path('ChangeSelect_3DObject/<int:pk>/', views.ChangeSelect_3DObject.as_view(), name="ChangeSelect_3DObject"),
    path('SavePly/', views.SavePly.as_view(), name="SavePly")
]
