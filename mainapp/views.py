from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import InitialObject, Object_3d
from .serilaizers import InitialObjectSerializer, Object_3DSerializer, Detail_3DSerializer, SavePlySerializer
import os
import shutil
from django.db import connections
from .camera.camClass import cameraApplications

@api_view(['POST'])
def execute_robot(request):
    try:
        id = request.data.get('id')
        obj = Object_3d.objects.filter(id=int(id)).first()
        serializer = Object_3DSerializer(obj, many=False)
        print(serializer.data.get('route'))
        return Response('ok', status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def open_camera(request):
    try:
        camRobot = cameraApplications()
        result, img_res_path = camRobot.capture("open")
        if result:
            return Response({"state": "ok", "image": img_res_path}, status=status.HTTP_200_OK)
        return Response({"state": "camera problem",}, status=status.HTTP_200_OK)
    except:
        return Response({"state": "error",}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def screen_shot(request):
    try:
        camRobot = cameraApplications()
        result, img_res_path = camRobot.capture("screen_shot")
        if result:
            return Response({"state": "ok", "image": img_res_path}, status=status.HTTP_200_OK)
        return Response({"state": "camera problem",}, status=status.HTTP_200_OK)
    except:
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def save_ply(request):
    try:
        camRobot = cameraApplications()
        result, _ = camRobot.capture("save_ply")
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

