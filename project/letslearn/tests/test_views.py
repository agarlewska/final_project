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
def test_material_detail(client, material, test_user, user_material):
    client.force_login(test_user)
    response = client.get(f'/materials/{material.id}/')
    assert response.status_code == 200
    assert response.context['material'][0].name == material.name

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
def test_user_material_detail(test_user, client, material, user_material):
    client.force_login(test_user)
    response = client.get(f'/materials/{material.id}/')
    assert response.status_code == 200
    assert response.context['material'][0] == material


@pytest.mark.django_db
def test_not_user_material_detail(test_user, test_user2, client, material, user_material):
    client.force_login(test_user2)
    # material = UserMaterial.objects.filter(user_id=test_user)[0]
    user = user_material.user_id
    response = client.get(f'/materials/{material.id}/')
    assert response.status_code == 200
    assert response.context['material'] == ''


@pytest.mark.django_db
def test_create_category(client, test_user):
    response = client.get('/category/create/', {'name': 'new'})
    assert response.status_code == 302
    client.force_login(user=test_user)
    response2 = client.get('/category/create/', {'name': 'new'})
    assert response2.status_code == 200
    response3 = client.post('/category/create/', {'name': 'new'})
    assert response3.status_code == 302
    assert Category.objects.get(name='new')


@pytest.mark.django_db
def test_create_platform(client, test_user):
    response = client.post('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 302
    client.force_login(user=test_user)
    response2 = client.get('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response2.status_code == 200
    response3 = client.post('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response3.status_code == 302
    assert Platform.objects.get(name='new')


@pytest.mark.django_db
def test_create_author(client, test_user):
    response = client.post('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 302
    # client.login(username=test_user.username, password=test_user.password)
    client.force_login(test_user)
    response2 = client.get('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response2.status_code == 200
    response2 = client.post('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response2.status_code == 302
    assert Author.objects.get(name='new')


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



# >>> response = c.get("/redirect_me/", follow=True)
# >>> response.redirect_chain
# [('http://testserver/next/', 302), ('http://testserver/final/', 302)]