import pytest
from django.urls import reverse

from project.letslearn.tests.conftest import author, platform, material


# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'view, www',
#     [
#         (author, 'author'),
#         (platform, 'platform'),
#         (material, 'materials'),
#     ],
# )
# def test_view_detail(client, view, www):
#     response = client.get(f'/{www}/{view.id}/')
#     assert response.status_code == 200
#     assert response.context['{view}'] == view


@pytest.mark.django_db
def test_author_detail(client, author):
    response = client.get(f'/author/{author.id}/')
    assert response.status_code == 200
    assert response.context['author'] == author

@pytest.mark.django_db

def test_platform_detail(client, platform):
    response = client.get(f'/platform/{platform.id}/')
    assert response.status_code == 200
    assert response.context['platform'] == platform


@pytest.mark.django_db
def test_material_detail(client, material):
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
def test_category_list_login(client, view_name):
    client.force_login(user='admin')
    response = client.get(reverse(view_name))
    assert response.status_code == 200
