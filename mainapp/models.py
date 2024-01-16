from django.db import models
from datetime import datetime
import os

class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def camera_image_path(instance, filename):
    return os.path.join('camera_image', str(instance.id), filename)

class InitialObject(Common):
    name = models.CharField(max_length=255, default=datetime.now().strftime('%Y/%m/%d %H:%M:%S'))    
    image_path = models.CharField(max_length=255, null=True, blank=True)
    ply_path = models.CharField(max_length=255, null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Object_3d(Common):
    date = models.CharField(max_length=225, null=True, blank=True)
    dotsCol = models.CharField(max_length=225, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    modelCol = models.CharField(max_length=225, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    rotation = models.CharField(max_length=225, null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    initial_objecte_id = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

class Route(Common):
    object_3d = models.ForeignKey(Object_3d, related_name='route', on_delete=models.CASCADE, null=True, blank=True)
    points = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return str(self.points)
    