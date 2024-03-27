from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import *
from .serilaizers import (InitialObjectSerializer, Object_3DSerializer, Detail_3DSerializer, SavePlySerializer,
                    DrawObjectSerializer)
import os
import shutil
from django.db import connections
# from .camera.camClass import cameraApplications
from .main.camClass import cameraApplications
from .main.camRobot import cameraRobot

@api_view(['POST'])
def execute_robot(request):
    try:
        # id = request.data.get('id')
        # obj = DrawObject.objects.filter(id=int(id)).first()
        # serializer = DrawObjectSerializer(obj, many=False)
        # data = serializer.data.get('point')

        # # robot
        # camRobot = cameraRobot()  
        # points = camRobot.parse_data(data, obj.initial_objecte_id)

        # real_position = camRobot.convert2real(points)

        # # os.system(camRobot.ethnet_command)     
        # camRobot.connect()
        # camRobot.send_robot_data(real_position)
        # # os.system(camRobot.wifi_command)

        print('手臂結束')
        return Response("ok", status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
import time
@api_view(['POST'])
def open_camera(request):
    try:
        time.sleep(2)
        result=True
        img_res_path = 'media/camera_data/62/1.jpg'

        # intel_camera
        # camRobot = cameraRobot('intel_camera')
        # result, img_res_path = camRobot.capture("open")
        
        # zivid
        # camRobot = cameraRobot()
        # os.system(camRobot.ethnet_command)
        # result, img_res_path = camRobot.capture("open")
        # os.system(camRobot.wifi_command)     

        if result:
            return Response({"state": "ok", "image": img_res_path}, status=status.HTTP_200_OK)
        return Response({"state": "camera problem",}, status=status.HTTP_200_OK)
    except:
        return Response({"state": "error",}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def screen_shot(request):
    try:
        time.sleep(2)
        result=True
        img_res_path = 'media/camera_data/62/5.jpg'

        # intel_camera
        # camRobot = cameraRobot('intel_camera')
        # result, img_res_path = camRobot.capture("screen_shot")

        # zivid
        # camRobot = cameraRobot()
        # os.system(camRobot.ethnet_command)
        # result, img_res_path = camRobot.capture("screen_shot")
        # os.system(camRobot.wifi_command)  
        
        if result:
            return Response({"state": "ok", "image": img_res_path}, status=status.HTTP_200_OK)
        return Response({"state": "camera problem",}, status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def save_ply(request):
    try:
        time.sleep(2)
        result=True
        print(request.data.get("inputText"))

        # intel_camera
        # camRobot = cameraRobot('intel_camera')
        # result, _ = camRobot.capture("save_ply")

        # zivid
        # camRobot = cameraRobot()
        # os.system(camRobot.ethnet_command)
        # result, _ = camRobot.capture("save_ply")
        # os.system(camRobot.wifi_command) 
        if result:
            obj = InitialObject.objects.filter(is_finished=True).last()
            serializer = InitialObjectSerializer(obj, many=False)
            return Response({"state": "ok", "obj_data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"state": "camera problem",}, status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def preprocessing_ply(request):
    try:
        name = request.data.get('name')
        init_obj = InitialObject.objects.filter(is_finished=True).last()
        if init_obj.name != name:
            print('asd')
            init_obj.name = name
            init_obj.save()
        return Response('ok', status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

# initial_object
@api_view(['GET'])
def get_initial_object(request):
    try:
        obj = InitialObject.objects.all().order_by('-id')
        serializer = InitialObjectSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def pin_initial_object(request, pk):
    try:
        init_obj = InitialObject.objects.filter(id=int(pk)).first()
        init_obj.is_pinned = request.data.get('is_pinned')
        init_obj.save()
        serializer = InitialObjectSerializer(init_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response('error',status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def select_initial_object(request, pk):
    try:
        InitialObject.objects.update(is_selected=False)
        init_obj = InitialObject.objects.filter(id=int(pk)).first()
        init_obj.is_selected = request.data.get('is_selected')
        init_obj.save()
        return Response('ok', status=status.HTTP_200_OK)
    except:
        Response('error',status=status.HTTP_400_BAD_REQUEST)

# draw_object
@api_view(['POST'])
def save_draw_object(request):
    try:
        '''
        order index 對應資料:
        "Point", "IrregularConti", "Line", "Square", 
        "Rectangle", "Polygon", "Circle", "Oval", "Arc"

        contiPoint 連續標點
        linePoint   形狀標點 Line
        squarePoint 形狀標點 Square
        '''
        data = request.data
        # del data['image']
        # print(data)

        if request.data.get('route', None) == None:
            
            obj = DrawObject.objects.create(
                date=request.data.get('date'),
                dotsCol=request.data.get('dotsCol'),
                image=request.data.get('image'),
                modelCol=request.data.get('modelCol'),
                name=request.data.get('name'),
                rotation=request.data.get('rotation'),
                initial_object_id=request.data.get('id'),
                        )

            for i in request.data.get('order'):
                Order.objects.create(
                    draw_object = obj,
                    index= i.get('index')
                )
            
            for i in request.data.get('point'):
                Point.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )

            for i in request.data.get('contiPoint'):
                ContiPoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )

            for i in request.data.get('linePoint'):
                LinePoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )

            for i in request.data.get('squarePoint'):
                SquarePoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )
            
            for i in request.data.get('polygonPoint'):
                PolygonPoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )

            for i in request.data.get('recPoint'):
                RecPoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )

            for i in request.data.get('circlePoint'):
                CirclePoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )

            for i in request.data.get('ovalPoint'):
                OvalPoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )

            for i in request.data.get('arcPoint'):
                ArcPoint.objects.create(
                    draw_object = obj,
                    points = i.get('points')
                )
        return Response('', status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_draw_object(request):
    try:
        obj = DrawObject.objects.all().order_by('-id')
        serializer = DrawObjectSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def get_single_draw_object(request, pk):
    try:
        obj = DrawObject.objects.filter(id=int(pk)).first()
        if request.method == 'GET':
            serializer = DrawObjectSerializer(obj, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            # 若是從showScreen傳過來
            if len(request.data) != 2:
                obj.dotsCol = request.data.get('dotsCol'),
                obj.modelCol = request.data.get('modelCol'),
                obj.name = request.data.get('name'),
                obj.rotation = request.data.get('rotation'),
                obj.save()

                orders = Order.objects.filter(draw_object=obj)
                points = Point.objects.filter(draw_object=obj)
                contiPoints = ContiPoint.objects.filter(draw_object=obj)
                linePoints = LinePoint.objects.filter(draw_object=obj)
                squarePoints = SquarePoint.objects.filter(draw_object=obj)
                polygonPoints = PolygonPoint.objects.filter(draw_object=obj)
                recPoints = RecPoint.objects.filter(draw_object=obj)
                circlePoints = CirclePoint.objects.filter(draw_object=obj)
                ovalPoints = OvalPoint.objects.filter(draw_object=obj)
                arcPoints = ArcPoint.objects.filter(draw_object=obj)

                for order in orders:
                    order.delete()
                for i in request.data.get('order'):
                    Order.objects.create(draw_object=obj, index=i)

                for point in points:
                    point.delete()
                for i in request.data.get('point'):
                    Point.objects.create(draw_object=obj, points=i.get('points'))

                for contiPoint in contiPoints:
                    contiPoint.delete()
                for i in request.data.get('contiPoint'):
                    ContiPoint.objects.create(draw_object=obj, points=i.get('points'))

                for linePoint in linePoints:
                    linePoint.delete()
                for i in request.data.get('linePoint'):
                    LinePoint.objects.create(draw_object=obj, points=i.get('points'))

                for squarePoint in squarePoints:
                    squarePoint.delete()
                for i in request.data.get('squarePoint'):
                    SquarePoint.objects.create(draw_object=obj, points=i.get('points'))
                
                for polygonPoint in polygonPoints:
                    polygonPoint.delete()
                for i in request.data.get('polygonPoint'):
                    PolygonPoint.objects.create(draw_object=obj, points=i.get('points'))

                for recPoint in recPoints:
                    recPoint.delete()
                for i in request.data.get('recPoint'):
                    RecPoint.objects.create(draw_object=obj, points=i.get('points'))
                
                for circlePoint in circlePoints:
                    circlePoint.delete()
                for i in request.data.get('circlePoint'):
                    CirclePoint.objects.create(draw_object=obj, points=i.get('points'))

                for ovalPoint in ovalPoints:
                    ovalPoint.delete()
                for i in request.data.get('ovalPoint'):
                    OvalPoint.objects.create(draw_object=obj, points=i.get('points'))

                for arcPoint in arcPoints:
                    arcPoint.delete()
                for i in request.data.get('arcPoint'):
                    ArcPoint.objects.create(draw_object=obj, points=i.get('points'))

            # 若是從showScreen傳過來只有 {'id': 41, 'order': [4, 2]}
            elif len(request.data) == 2:
                orders = Order.objects.filter(draw_object=obj)
                for order in orders:
                    order.delete()
                for i in request.data.get('order'):
                    Order.objects.create(draw_object=obj, index=i)
            return Response('ok', status=status.HTTP_200_OK)     
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def edit_draw_object_order(request):
    try:
        print('asdasdasd')
        print(request.data)
        # obj = DrawObject.objects.filter(id=int(1)).first()
        # obj.order = '123'
        # obj.save()
        return Response('success', status=status.HTTP_200_OK) 
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def pin_draw_object(request, pk):
    try:
        obj = DrawObject.objects.filter(id=int(pk)).first()
        obj.is_pinned = request.data.get('is_pinned')
        obj.save()
        serializer = DrawObjectSerializer(obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def select_draw_object(request, pk):
    try:
        DrawObject.objects.update(is_selected=False)
        obj = DrawObject.objects.filter(id=int(pk)).first()
        obj.is_selected = request.data.get('is_selected')
        obj.save()
        serializer = DrawObjectSerializer(obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

class initial_3D_object(APIView):
    def get(self, request):
        obj = InitialObject.objects.all()
        serializer = InitialObjectSerializer(obj, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        init_obj = InitialObject.objects.filter(is_finished=False).first()
        if init_obj:
            if request.data.get('state') == 'image':
                image_file = request.data.get('image_file')
                print(request.data)
                return Response('ok', status=200)
            else:
                init_obj.is_finished = True
                init_obj.save()
            return Response('ok', status=200)
        else:
            serializer = InitialObjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        return Response("error", status=400)
    
class initial_3D_object_detail(APIView):
    def get_object(self, pk):
        try:
            return InitialObject.objects.filter(id=int(pk)).first()
        except:
            return Response('error', status=400)
        
    def get(self, request, pk):
        data = self.get_object(pk)
        serializer = InitialObjectSerializer(data, many=False)
        return Response(serializer.data, status=200)
    
    def put(self, request, pk):
        data = self.get_object(pk)
        serializer = InitialObjectSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response('error', status=400)
    
    def delete(self, request, pk):
        data = self.get_object(pk)
        data.delete()
        return Response({'delete'}, status=204)

class get_object_3d(viewsets.ModelViewSet):
    serializer_class = Object_3DSerializer
    queryset = Object_3d.objects.all().order_by('-id')

# def ConvertToObj(path = r"C:\Users\User\Downloads\Input.ply",
#                  o_path = r"C:\Users\danie\Output.obj"):
#     scene = a3d.Scene.from_file(path)
#     scene.save(o_path)
    
class Generate_3D_object(APIView):
    def post(self, request, format=None):
        # bun_zipper.ply  metal-table.ply
        file_name = 'bun_zipper.ply'
        ply_file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        obj_file_path = os.path.join(settings.MEDIA_ROOT, file_name.replace('.ply', '.obj'))
        # if not os.path.exists(obj_file_path):
        #     ConvertToObj(ply_file_path, obj_file_path)
        obj_url = request.build_absolute_uri(settings.MEDIA_URL + file_name.replace('.ply', '.obj'))

        file_name2 = 'metal-table.ply'
        obj_url2 = request.build_absolute_uri(settings.MEDIA_URL + file_name2.replace('.ply', '.obj'))
        return Response({'obj_file_path': obj_url, 'obj_file_path2': obj_url2})
    
class Detail_3D_object(APIView): 
    def get(self, request, pk, format=None):
        obj = Object_3d.objects.filter(id=pk).first()
        seriailzer = Detail_3DSerializer(obj)
        
        # if pk == 13 or pk == 17:
        #     file_name = 'bun_zipper.ply'
        # elif pk == 14:
        #     file_name = 'gear.ply'
        # elif pk == 15:
        #     file_name = 'Motorcycle_cylinder_head.ply'
        # obj_url = request.build_absolute_uri(settings.MEDIA_URL + file_name.replace('.ply', '.obj'))
        file_name = obj.name + '.ply'
        obj_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
        data = seriailzer.data
        data['obj_url'] =  obj_url
        print(obj_url)
        return Response(data)
    
    def put(self, request, pk, format=None):
        obj = Object_3d.objects.filter(id=pk).first()
        serializer = Detail_3DSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangeSelect_3DObject(APIView):
    def put(self, request, pk, format=None):
        Object_3d.objects.update(is_selected=False)
        obj = Object_3d.objects.filter(id=pk).first()
        serializer = Detail_3DSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class test(APIView):
    def post(self, request, format=None):
        obj = Object_3d.objects.filter(id=13).values('id', 'route')
        # print(obj)
        with connections['externalDB'].cursor() as cursor:
            cursor.execute("INSERT INTO object (points_id) VALUES (%s)", [3])
        
        temp = [
             [3, 9.4193, 7.1033, 19.7613],
             [3, -7.5942, 13.5902, 18.7572],
             [3, -7.8117, -7.0109, 30.8294],
             ]
        
        for t in temp:
            with connections['externalDB'].cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO points (object_id, x, y, z) VALUES (%s, %s, %s, %s)",
                            [t[0], t[1], t[2], t[3]]
                        )
        return Response({'obj_file_path': 'ok'})

class SavePly(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = SavePlySerializer(data=request.data)
        if serializer.is_valid():
            uploaded_blob = serializer.validated_data['blob']
            file_path = os.path.join(settings.MEDIA_ROOT, 'ply', 'zxc.ply')
            with open(file_path, 'wb') as destination_file:
                for chunk in uploaded_blob.chunks():
                    destination_file.write(chunk)
            return Response({'message': 'uplaod success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

