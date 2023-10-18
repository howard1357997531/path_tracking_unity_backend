from rest_framework import serializers
from .models import Object_3d, Route

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['points']

class Object_3DSerializer(serializers.ModelSerializer):
    route = RouteSerializer(many=True, required=False)

    class Meta:
        model = Object_3d
        fields = ('id', 'date', 'dotsCol', 'image', 'modelCol', 'name', 'rotation', 'is_pinned', "is_selected", 'route')
    
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