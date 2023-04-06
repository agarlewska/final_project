import pytest
from django.test import Client
from letslearn.models import Platform, Category, Author, MaterialType, TrainingMaterials


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def author():
    return Author.objects.create(name='surname', www='adress', comment='many comments')


@pytest.fixture
def platform():
    return Platform.objects.create(name='name', www='adress', comment='many comments')


@pytest.fixture
def category():
    return Category.objects.create(name='name')


@pytest.fixture
def material_type():
    return MaterialType.objects.create(name='name')

@pytest.fixture
def material(author, material_type, platform):
    return TrainingMaterials.objects.create(name='name', is_time_limited=False, is_finished=False, author_id=author.id, material_type_id=material_type.id, platform_id=platform.id)
