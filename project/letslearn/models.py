from django.conf import settings
from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=256, unique=True)
    www = models.CharField(max_length=256, null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_details')


class Platform(models.Model):
    name = models.CharField(max_length=128, unique=True)
    www = models.CharField(max_length=256)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('platform_list')

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list')


class MaterialType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class TrainingMaterials(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    www = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    is_time_limited = models.BooleanField()
    expiration_date = models.DateField(default='9999-12-31')
    is_finished = models.BooleanField()
    comment = models.TextField(null=True)
    expected_study_time = models.IntegerField(null=True)
    is_archived = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('material_list')

    def __str__(self):
        return self.name


class UserMaterial(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material_id = models.ForeignKey(TrainingMaterials, on_delete=models.CASCADE)
