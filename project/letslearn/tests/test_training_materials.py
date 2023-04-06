import pytest

@pytest.mark.django_db
def test_material_detail(client, material):
    response = client.get(f'/materials/{material.id}/')
    assert response.status_code == 200
    # assert response.context['name'] == platform.name
    assert response.context['material'] == material