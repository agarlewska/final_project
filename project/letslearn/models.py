from django.conf import settings
from django.db import models
from django.urls import reverse


class Author(models.Model):
    """Stores information about author of training material."""
    name = models.CharField(max_length=256, unique=True)
    www = models.CharField(max_length=256, null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        """Shows name of the author."""
        return self.name

    def get_absolute_url(self):
        """Redirect to author details"""
        return reverse('author_details')


class Platform(models.Model):
    """Stores information about platform with training material."""
    name = models.CharField(max_length=128, unique=True)
    www = models.CharField(max_length=256)
    comment = models.TextField(null=True)

    def __str__(self):
        """Shows name of the platform."""
        return self.name

    def get_absolute_url(self):
        """Redirect to platforms' list"""
        return reverse('platform_list')


class Category(models.Model):
    """Stores information about category of training material."""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        """Shows name of the category."""
        return self.name

    def get_absolute_url(self):
        """Redirect to categories' list"""
        return reverse('category_list')


class MaterialType(models.Model):
    """Stores information about type of training material."""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        """Shows name of the type of material."""
        return self.name


class TrainingMaterials(models.Model):
    """Stores information about training material, related to: :model:`letslearn.Author,
     :model:`letslearn.Platform`, :model:`letslearn.Category`, :model:`letslearn.MaterialType`,
     model:`letslearn.Category`.
     """
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

    def __str__(self):
        """Shows name of the type of material."""
        return self.name

    def get_absolute_url(self):
        """Redirect to materials' list"""
        return reverse('material_list')


class UserMaterial(models.Model):
    """Model that connects user with material, related to :model:`auth.User and :model:`letslearn.TrainingMaterials."""
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material_id = models.ForeignKey(TrainingMaterials, on_delete=models.CASCADE)



    """Return a foobang

    Optional plotz says to frobnicate the bizbaz first.
    """