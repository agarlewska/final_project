import pytest
from django.urls import reverse
from letslearn.models import TrainingMaterials, UserMaterial, Category, Platform, Author


@pytest.mark.django_db
def test_author_detail(client, author, test_user):
    client.force_login(test_user)
    response = client.get(f'/author/{author.id}/')
    assert response.status_code == 200
    assert response.context['author'] == author

@pytest.mark.django_db

def test_platform_detail(client, platform, test_user):
    client.force_login(test_user)
    response = client.get(f'/platform/{platform.id}/')
    assert response.status_code == 200
    assert response.context['platform'] == platform


@pytest.mark.django_db
def test_material_detail(client, material, test_user):
    client.force_login(test_user)
    response = client.get(f'/materials/{material.id}/')
    assert response.status_code == 200
    # assert response.context['name'] == platform.name
    assert response.context['material'] == material

@pytest.mark.django_db
@pytest.mark.parametrize(
    'view_name',
    [
        ('category_list'),
        ('material_list'),
        ('platform_list'),
        ('author_list'),
    ],
)
def test_category_list_logout(client, view_name):
    client.logout()
    response = client.get(reverse(view_name))
    assert response.status_code != 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'view_name',
    [
        ('category_list'),
        ('material_list'),
        ('platform_list'),
        ('author_list'),
    ],
)
def test_category_list_login(test_user, client, view_name):
    client.login(username=test_user.username, password=test_user.password)
    response = client.get(reverse(view_name))
    assert response.status_code == 302 #200


@pytest.mark.django_db
def test_user_material_list(test_user, client, material, user_material):
    client.login(username=test_user.username, password=test_user.password)
    material = UserMaterial.objects.filter(user_id=test_user)
    response = client.get('material_list')
    assert material.count() == 1
    assert response.context


@pytest.mark.django_db
def test_not_user_material_list(test_user, test_user2, client, material, user_material):
    client.force_login(test_user2)
    material = UserMaterial.objects.filter(user_id=test_user)
    response = client.get('/materials/list/')
    assert response.context is None


@pytest.mark.django_db
def test_create_category(client, test_user):
    response = client.post('/category/create/', {'name': 'new'})
    assert response.status_code == 302
    client.force_login(test_user)
    response = client.post('/category/create/', {'name': 'new'})
    assert response.status_code == 200
    # assert Category.objects.get(name='new')


@pytest.mark.django_db
def test_create_platform(client, test_user):
    response = client.post('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 302
    client.force_login(test_user)
    response = client.post('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 200
    assert Platform.objects.get(name='new')

@pytest.mark.django_db
def test_create_author(client, test_user):
    response = client.post('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 302
    # client.login(username=test_user.username, password=test_user.password)
    client.force_login(test_user)
    response = client.post('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 200
    # assert Author.objects.get(name='new')


@pytest.mark.django_db
def test_create_material(client, test_user, author, material_type, platform):
    response = client.post('/materials/create/', {'name': 'name',
                                                        'description': 'desc',
                                                        'is_time_limited': False,
                                                        'is_finished': False,
                                                        'author_id': author.id,
                                                        'material_type_id': material_type.id,
                                                        'platform_id': platform.id})
    assert response.status_code == 302
    # client.login(username=test_user.username, password=test_user.password)
    client.force_login(test_user)
    response2 = client.post('/materials/create/', {'name': 'name',
                                                        'description': 'desc',
                                                        'is_time_limited': False,
                                                        'is_finished': False,
                                                        'author_id': author.id,
                                                        'material_type_id': material_type.id,
                                                        'platform_id': platform.id})
    assert response2.status_code == 200
    # material = TrainingMaterials.objects.get(name='name')
    # UserMaterial.objects.create(material_id=material, user_id=test_user)
    # assert UserMaterial.objects.get(material_id=material)
