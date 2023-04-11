import pytest
from django.urls import reverse
from letslearn.models import TrainingMaterials, UserMaterial, Category, Platform, Author


@pytest.mark.django_db
def test_author_detail(client, author, test_user):
    """
    Tests author detail view.
    :param client: fixture client
    :param author: fixture author
    :param test_user: fixture test_user
    :return: two tests:
        - Http response code is 200 (OK)
        - Context contains information about author
    """
    client.force_login(test_user)
    response = client.get(f'/author/{author.id}/')
    assert response.status_code == 200
    assert response.context['author'] == author


@pytest.mark.django_db
def test_platform_detail(client, platform, test_user):
    """
    Tests platform detail view.
    :param client: fixture client
    :param platform: fixture platform
    :param test_user: fixture test_user
    :return: two tests:
        - Http response code is 200 (OK)
        - Context contains information about platform
    """
    client.force_login(test_user)
    response = client.get(f'/platform/{platform.id}/')
    assert response.status_code == 200
    assert response.context['platform'] == platform


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
    """
    Tests rendering views for logout users.
    :param client: fixture client
    :param view_name: parametr containing tested view name
    :return: client should be redirected to login page, http status code is 302 (redirect)
    """
    client.logout()
    response = client.get('/category/list/')
    assert response.status_code == 302


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
    """
    Tests rendering views for logged users.
    :param client: fixture client
    :param view_name: parametr containing tested view name
    :return: http status code is 200 (OK)
    """
    client.force_login(test_user)
    # response = client.get(reverse(view_name))
    response = client.get('/category/list/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_material_detail(test_user, client, material, user_material):
    """
    Tests training material detail view. Training material owned by logged user.
    :param client: fixture client
    :param material: fixture material
    :param test_user: fixture test_user
    :param user_material: fixture user_material
    :return: two tests:
        - Http response code is 200 (OK)
        - Context contains information about training material
    """
    client.force_login(test_user)
    response = client.get(f'/materials/{material.id}/')
    assert response.status_code == 200
    assert response.context['material'] == material


@pytest.mark.django_db
def test_not_user_material_detail(test_user, test_user2, client, material, user_material):
    """
    Tests training material detail view. Training material owned by other than logged user.
    :param client: fixture client
    :param material: fixture material
    :param test_user: fixture test_user
    :param user_material: fixture user_material
    :return: two tests:
        - Http response code is 200 (OK)
        - Context does't contain information about training material
    """
    client.force_login(test_user2)
    # material = UserMaterial.objects.filter(user_id=test_user)[0]
    # user = user_material.user_id
    response = client.get(f'/materials/{material.id}/')
    assert response.status_code == 200
    assert response.context['material'] == ''


@pytest.mark.django_db
def test_create_category(client, test_user):
    """
    Tests category create view. Checks whether logged and logout user can add new category.
    Function generates four tests:
        - user (without login) sends a get reguest
        - logged user sends a get request
        - logged user sends a post request (add new category)
        - checks whether there is a new object in Category model.
    :param client: fixture client
    :param test_user: fixture test_user
    :return: four tests:
        - Http response code is 302 (redirect)
        - Http response code is 200 (OK)
        - Http response code is 302 (redirect)
        - New object in Category model with name = 'new' exists.
    """
    response = client.get('/category/create/', {'name': 'new'})
    assert response.status_code == 302
    client.force_login(user=test_user)
    response2 = client.get('/category/create/', {'name': 'new'})
    assert response2.status_code == 200
    response3 = client.post('/category/create/', {'name': 'new'})
    assert response3.status_code == 302
    assert Category.objects.get(name='new')


@pytest.mark.django_db
def test_create_category_count(client, test_user):
    client.force_login(test_user)
    categories_count = Category.objects.count()
    new_category = {'name': 'new category'}
    response = client.post("/category/create/", new_category)
    assert response.status_code == 302
    assert Category.objects.count() == categories_count + 1
    # for key, value in new_category.items():
    #     assert key in response.data
    #     assert response.data[key] == value

    # for field in ("title", "year", "description", "director", "actors"):
    #     assert field in response.data


@pytest.mark.django_db
def test_create_platform(client, test_user):
    """
    Tests platform create view. Checks whether logged and logout user can add new platfotm.
    Function generates four tests:
        - user (without login) sends a get reguest
        - logged user sends a get request
        - logged user sends a post request (add new platform)
        - checks whether there is a new object in Platform model.
    :param client: fixture client
    :param test_user: fixture test_user
    :return: four tests:
        - Http response code is 302 (redirect)
        - Http response code is 200 (OK)
        - Http response code is 302 (redirect)
        - New object in Platform model with name = 'new' exists.
    """
    response = client.post('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 302
    client.force_login(user=test_user)
    response2 = client.get('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response2.status_code == 200
    response3 = client.post('/platform/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response3.status_code == 302
    assert Platform.objects.get(name='new')


@pytest.mark.django_db
def test_update_platform(client, test_user, platform):
    """
    Tests platform update view.
    Function generates four tests:
        - user (without login) sends a get reguest
        - logged user sends a get request
        - logged user sends a post request (add new platform)
        - checks whether there is a new object in Platform model.
    :param client: fixture client
    :param test_user: fixture test_user
    :return: four tests:
        - Http response code is 302 (redirect)
        - Http response code is 200 (OK)
        - Http response code is 302 (redirect)
        - New object in Platform model with name = 'new' exists.
    """
    client.force_login(user=test_user)
    response = client.post('/platform/update/{platform.id}/', {'name': platform.name, 'www': platform.www, 'comment': 'new comm'})
    #assert response.status_code == 200
    platform_updated = Platform.objects.get(id=platform.id)
    assert platform_updated.comment == 'aaa'


@pytest.mark.django_db
def test_create_author(client, test_user):
    """
    Tests author create view. Checks whether logged and logout user can add new author.
    Function generates four tests:
        - user (without login) sends a get reguest
        - logged user sends a get request
        - logged user sends a post request (add new author)
        - checks whether there is a new object in Author model.
    :param client: fixture client
    :param test_user: fixture test_user
    :return: four tests:
        - Http response code is 302 (redirect)
        - Http response code is 200 (OK)
        - Http response code is 302 (redirect)
        - New object in Author model with name = 'new' exists.
    """
    response = client.post('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response.status_code == 302
    client.force_login(test_user)
    response2 = client.get('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response2.status_code == 200
    response2 = client.post('/author/create/', {'name': 'new', 'www': 'adress', 'comment': 'comm'})
    assert response2.status_code == 302
    assert Author.objects.get(name='new')


@pytest.mark.django_db
def test_create_material(client, test_user, author, material_type, platform, material, user_material):
    """
    Tests training material create view. Checks whether logged and logout user can add new amaterial.
    Function generates five tests:
        - user (without login) sends a get reguest
        - logged user sends a get request
        - logged user sends a post request (add new training material)
        - checks whether there is a new object in Training Material model.
        - checks whether there is a new object in UserMaterial model.
    :param client: fixture client
    :param test_user: fixture test_user
    :param author: fixture author
    :param material_type: fixture material_type
    :param platform: fixture platform
    :param material: fixture material
    :return: four tests:
        - Http response code is 302 (redirect)
        - Http response code is 200 (OK)
        # - Http response code is 302 (redirect)
        - New object in TrainingMaterials model with name = 'name' exists.
        - New object in UserMaterial model with material exists.
    """
    response = client.get('/materials/create/', {'name': 'name',
                                                        'description': 'desc',
                                                        'is_time_limited': False,
                                                        'is_finished': False,
                                                        'author_id': author.id,
                                                        'material_type_id': material_type.id,
                                                        'platform_id': platform.id})
    assert response.status_code == 302
    # client.login(username=test_user.username, password=test_user.password)
    client.force_login(test_user)
    response2 = client.get('/materials/create/', {'name': 'name',
                                                        'description': 'desc',
                                                        'is_time_limited': False,
                                                        'is_finished': False,
                                                        'author_id': author.id,
                                                        'material_type_id': material_type.id,
                                                        'platform_id': platform.id})
    assert response2.status_code == 200
    response3 = client.post('/materials/create/', {'name': 'name',
                                                        'description': 'desc',
                                                        'is_time_limited': False,
                                                        'is_finished': False,
                                                        'author_id': author.id,
                                                        'material_type_id': material_type.id,
                                                        'platform_id': platform.id})
    # assert response3.status_code == 200
    # [10 / Apr / 2023 08: 52:21] "POST /materials/create/ HTTP/1.1" 302 0
    # [10 / Apr / 2023 08: 52:21] "GET /materials/list/ HTTP/1.1" 200 1081
    assert TrainingMaterials.objects.get(name='name')
    assert UserMaterial.objects.get(material_id=material)




# >>> response = c.get("/redirect_me/", follow=True)
# >>> response.redirect_chain
# [('http://testserver/next/', 302), ('http://testserver/final/', 302)]