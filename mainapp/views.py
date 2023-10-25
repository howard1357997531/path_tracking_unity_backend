from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Object_3d
from .serilaizers import Object_3DSerializer, Detail_3DSerializer, SavePlySerializer
# import aspose.threed as a3d
import os
from django.db import connections

# @api_view(['GET'])
# def get_object_3d(request):
#     products = object_3d.objects.all()
#     serializer = object_3dSerializer(products, many=True)
#     return Response(serializer.data)

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

