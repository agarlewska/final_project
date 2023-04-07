import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import Client
from letslearn.models import Platform, Category, Author, MaterialType, TrainingMaterials, UserMaterial


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


@pytest.fixture
def test_user():
    user = User.objects.create_user(username='user00', password='rQw_PQssw0rd')
    return user


@pytest.fixture
def user_material(test_user, material):
    return UserMaterial.objects.create(user_id=test_user, material_id=material)


@pytest.fixture
def test_user2():
    user = User.objects.create_user(username='user01', password='rQw_PQssw0rd')
    return user

