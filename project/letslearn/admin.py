from django.contrib import admin
from .models import Author, Category, MaterialType, Platform, TrainingMaterials, UserMaterial


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(MaterialType)
admin.site.register(Platform)
admin.site.register(TrainingMaterials)
admin.site.register(UserMaterial)
