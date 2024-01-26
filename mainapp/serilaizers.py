from rest_framework import serializers
from .models import *

class InitialObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialObject
        fields = '__all__'
        # fields = ('id', 'name', 'ply_file', 'camera_image')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['index']

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['points']

class ContiPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContiPoint
        fields = ['points']

class LinePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinePoint
        fields = ['points']

class SquarePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = SquarePoint
        fields = ['points']

class PolygonPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonPoint
        fields = ['points']

class RecPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecPoint
        fields = ['points']

class CirclePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CirclePoint
        fields = ['points']

class OvalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = OvalPoint
        fields = ['points']

class ArcPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArcPoint
        fields = ['points']        

class DrawObjectSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=True, required=False)
    point = PointSerializer(many=True, required=False)
    contiPoint = ContiPointSerializer(many=True, required=False)
    linePoint = LinePointSerializer(many=True, required=False)
    squarePoint = SquarePointSerializer(many=True, required=False)
    polygonPoint = PolygonPointSerializer(many=True, required=False)
    recPoint = RecPointSerializer(many=True, required=False)
    circlePoint = CirclePointSerializer(many=True, required=False)
    ovalPoint = OvalPointSerializer(many=True, required=False)
    arcPoint = ArcPointSerializer(many=True, required=False)
    class Meta:
        model = DrawObject
        fields = ('id', 'date', 'dotsCol', 'image', 'modelCol', 'name', 'rotation', 
                  'is_pinned', 'is_selected', 'initial_object_id', 'order', 'point', 'contiPoint',
                  'linePoint', 'squarePoint' , 'polygonPoint', 'recPoint', 'circlePoint',
                  'ovalPoint', 'arcPoint')

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['points']

class Object_3DSerializer(serializers.ModelSerializer):
    route = RouteSerializer(many=True, required=False)

    class Meta:
        model = Object_3d
        fields = ('id', 'date', 'dotsCol', 'image', 'modelCol', 'name', 'rotation', 
                  'is_pinned', 'is_selected', 'initial_objecte_id', 'route')
    
    def create(self, validated_data):
        # print(validated_data)
        route_data = validated_data.pop('route', None)
        object_3d = Object_3d.objects.create(**validated_data)

        if route_data:
            for route_item in route_data:
                Route.objects.create(object_3d=object_3d, **route_item)

        return object_3d
    
    def update(self, instance, validated_data):
        route_data = validated_data.pop('route', None)
        
        instance = super().update(instance, validated_data)  # 呼叫父類的update方法更新其他字段

        if route_data:
            # 先刪除
            routes = Route.objects.filter(object_3d=instance)
            for route in routes:
                route.delete()
            # 再新增
            for route_item in route_data:
                Route.objects.create(object_3d=instance, **route_item)

        return instance
    
class Detail_3DSerializer(serializers.ModelSerializer):
    route = RouteSerializer(many=True, required=False)

    class Meta:
        model = Object_3d
        fields = ('id', 'date', 'dotsCol', 'image', 'modelCol', 'name', 'rotation', 'is_pinned', "is_selected", 'route')
    
    def update(self, instance, validated_data):
        route_data = validated_data.pop('route', None)
        
        instance = super().update(instance, validated_data)  # 呼叫父類的update方法更新其他字段

        if route_data:
            # 先刪除
            routes = Route.objects.filter(object_3d=instance)
            for route in routes:
                route.delete()
            # 再新增
            for route_item in route_data:
                Route.objects.create(object_3d=instance, **route_item)

        return instance

class SavePlySerializer(serializers.Serializer):
    blob = serializers.FileField()