import pytest

@pytest.mark.django_db
def test_material_type_detail(client, platform):
    response = client.get(f'/platform/{platform.id}/')
    assert response.status_code == 200
    assert response.context['platform'] == platform
