from django.db import models

class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Object_3d(Common):
    date = models.CharField(max_length=225, null=True, blank=True)
    dotsCol = models.CharField(max_length=225, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    modelCol = models.CharField(max_length=225, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    rotation = models.CharField(max_length=225, null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Route(Common):
    object_3d = models.ForeignKey(Object_3d, related_name='route', on_delete=models.CASCADE, null=True, blank=True)
    points = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return str(self.points)
    