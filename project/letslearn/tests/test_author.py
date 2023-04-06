import pytest

@pytest.mark.django_db
def test_author_detail(client, author):
    response = client.get(f'/author/{author.id}/')
    assert response.status_code == 200
    assert response.context['author'] == author
