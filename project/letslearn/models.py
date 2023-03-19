from django.conf import settings
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=256, unique=True)
    information = models.CharField(max_length=256)
    comment = models.TextField()

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=128, unique=True)
    information = models.CharField(max_length=256)
    comment = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class MaterialType(models.Model):
    name = models.CharField(max_length=64, unique=True)


class TeachingMaterials(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    url = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    time_limited = models.BooleanField()
    expiration_date = models.DateField()
    finished = models.BooleanField()
    comments = models.TextField()
    exp_study_time = models.IntegerField()


class UserMaterial(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material_id = models.ForeignKey(TeachingMaterials, on_delete=models.CASCADE)
