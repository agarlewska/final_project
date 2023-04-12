import random

import pytest
from faker import Faker
from django.urls import reverse
from letslearn.models import TrainingMaterials, UserMaterial, Category, Platform, Author

faker = Faker()

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
    new_name = faker.word()
    response = client.get('/category/create/', {'name': new_name})
    assert response.status_code == 302
    client.force_login(user=test_user)
    response2 = client.get('/category/create/', {'name': new_name})
    assert response2.status_code == 200
    response3 = client.post('/category/create/', {'name': new_name})
    assert response3.status_code == 302
    assert Category.objects.get(name=new_name)


@pytest.mark.django_db
def test_create_category_count(client, test_user):
    client.force_login(test_user)
    categories_count = Category.objects.count()
    new_category_name = faker.word()
    new_category = {'name': new_category_name}
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
    new_name = faker.word()
    new_www = faker.url()
    new_comment = faker.sentence()
    response = client.post('/platform/create/', {'name': new_name, 'www': new_www, 'comment': new_comment})
    assert response.status_code == 302
    client.force_login(user=test_user)
    response2 = client.get('/platform/create/', {'name': new_name, 'www': new_www, 'comment': new_comment})
    assert response2.status_code == 200
    response3 = client.post('/platform/create/', {'name': new_name, 'www': new_www, 'comment': new_comment})
    assert response3.status_code == 302
    assert Platform.objects.get(name=new_name)


@pytest.mark.django_db
def test_update_platform(client, test_user, platform):
    """
    Tests platform update view.
    Function generates two tests:
        - logged user sends a post request with new platform data (new comment)
        - checks whether new object in Platform model has attributes like selected in request.
    :param client: fixture client
    :param test_user: fixture test_user
    :return: two tests:
        - Http response code is 302 (redirect)
        - Updated instance of Platform model has new comment value.
    """
    client.force_login(user=test_user)
    new_comment = faker.sentence()
    platform_details = {'name': platform.name, 'www': platform.www, 'comment': new_comment}
    response = client.post(f'/platform/update/{platform.id}/', platform_details)
    assert response.status_code == 302
    platform_updated = Platform.objects.get(id=platform.id)
    assert platform_updated.comment == new_comment


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
    new_name = faker.word()
    new_www = faker.url()
    new_comment = faker.sentence()
    response = client.post('/author/create/', {'name': new_name, 'www': new_www, 'comment': new_comment})
    assert response.status_code == 302
    client.force_login(test_user)
    response2 = client.get('/author/create/', {'name': new_name, 'www': new_www, 'comment': new_comment})
    assert response2.status_code == 200
    response2 = client.post('/author/create/', {'name': new_name, 'www': new_www, 'comment': new_comment})
    assert response2.status_code == 302
    assert Author.objects.get(name=new_name)


@pytest.mark.django_db
def test_update_author(client, test_user, author):
    """
    Tests author update view.
    Function generates two tests:
        - logged user sends a post request with new author data (new www)
        - checks whether new instance in Author model has attributes like selected in request.
    :param client: fixture client
    :param test_user: fixture test_user
    :param author: fixture author
    :return: two tests:
        - Http response code is 302 (redirect)
        - Updated instance of Author model has new www value.
    """
    client.force_login(user=test_user)
    new_www = faker.url()
    author_details = {'name': author.name, 'www': new_www, 'comment': author.comment}
    response = client.post(f'/author/update/{author.id}/', author_details)
    assert response.status_code == 302
    author_updated = Author.objects.get(id=author.id)
    assert author_updated.www == new_www


# @pytest.mark.django_db
# def test_create_material(client, test_user, author, material_type, platform):
#     """
#     Tests training material create view. Checks whether logged and logout user can add new amaterial.
#     Function generates five tests:
#         - user (without login) sends a get reguest
#         - logged user sends a get request
#         - logged user sends a post request (add new training material)
#         - checks whether there is a new object in Training Material model.
#         - checks whether there is a new object in UserMaterial model.
#     :param client: fixture client
#     :param test_user: fixture test_user
#     :param author: fixture author
#     :param material_type: fixture material_type
#     :param platform: fixture platform
#     :param material: fixture material
#     :return: four tests:
#         - Http response code is 302 (redirect)
#         - Http response code is 200 (OK)
#         # - Http response code is 302 (redirect)
#         - New object in TrainingMaterials model with name = 'name' exists.
#         - New object in UserMaterial model with material exists.
#     """
#     name = 'new_name'
#     description = 'new_desc'
#     is_time_limited = False
#     is_finished= False
#     response = client.get('/materials/create/', {'name': name,
#                                                         'description': description,
#                                                         'is_time_limited': is_time_limited,
#                                                         'is_finished': is_finished,
#                                                         'author_id': author.id,
#                                                         'material_type_id': material_type.id,
#                                                         'platform_id': platform.id})
#     assert response.status_code == 302
#     # client.login(username=test_user.username, password=test_user.password)
#     client.force_login(test_user)
#     response2 = client.get('/materials/create/', {'name': name,
#                                                         'description': description,
#                                                         'is_time_limited': is_time_limited,
#                                                         'is_finished': is_finished,
#                                                         'author_id': author.id,
#                                                         'material_type_id': material_type.id,
#                                                         'platform_id': platform.id})
#     assert response2.status_code == 200
#     response3 = client.post('/materials/create/', {'name': name,
#                                                         'description': description,
#                                                         'is_time_limited': is_time_limited,
#                                                         'is_finished': is_finished,
#                                                         'author_id': author.id,
#                                                         'material_type_id': material_type.id,
#                                                         'platform_id': platform.id})
#     # assert response3.status_code == 200
#     # [10 / Apr / 2023 08: 52:21] "POST /materials/create/ HTTP/1.1" 302 0
#     # [10 / Apr / 2023 08: 52:21] "GET /materials/list/ HTTP/1.1" 200 1081
#     new_material = TrainingMaterials.objects.get(name=name)
#     assert new_material
#     assert UserMaterial.objects.get(material_id=new_material)


@pytest.mark.django_db
def test_create_material(client, test_user, author, material_type, platform, category):
    """
    Tests training material adding new materials to database.
    :param client: fixture client
    :param test_user: fixture test_user
    :param author: fixture author
    :param material_type: fixture material_type
    :param platform: fixture platform
    :param category: fixture category
    :return: four tests:
        - Http response code is 302 (redirect)
        - Http response code is 200 (OK)
        # - Http response code is 302 (redirect)
        - New object in TrainingMaterials model with name = 'name' exists.
        - New object in UserMaterial model with material exists.
    """
    new_name = faker.sentence(3)
    expiration_date = faker.date()
    new_material = TrainingMaterials.objects.create(name= new_name,
                        description= faker.sentence(),
                        www= faker.url(),
                        is_time_limited= faker.boolean(),
                        expiration_date= expiration_date,
                        is_finished= faker.boolean(),
                        expected_study_time= random.randint(1,100),
                        author_id= author.id,
                        material_type_id= material_type.id,
                        platform_id= platform.id,
                        is_archived= faker.boolean())
    new_material.category.set([category.id])
    new_material_from_db = TrainingMaterials.objects.get(name=new_name)
    assert new_material_from_db


# >>> response = c.get("/redirect_me/", follow=True)
# >>> response.redirect_chain
# [('http://testserver/next/', 302), ('http://testserver/final/', 302)]