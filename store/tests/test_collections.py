from store.models import Collection
from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture
def creat_collection(api_client):
    # if we pass collection inside the create collection args it will be considered to be a fixture
    # to solve this we use an inner function
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymus_returns_401(self, creat_collection):
        response = creat_collection({"title": "a"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, creat_collection):
        authenticate()
        response = creat_collection({"title": "a"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, creat_collection):
        # Arange
        authenticate(is_staff=True)
        # Act
        response = creat_collection({"title": ""})
        # Assertion
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, creat_collection):
        authenticate(is_staff=True)
        response = creat_collection({"title": "a"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exsists_returns_200(self, api_client):
        # Arrange
        # This is against the Rule of Testing behaviours rather than the Implementation but we have no other choice
        # we can also use api_client to send a post request first instead of the line below but that approach has a lot of bugs
        # Collection.objects.create(title="a")
        # a better approach so that we do not have to create all of the fields is to use model bakery like this :
        collection = baker.make(Collection)

        response = api_client.get(f"/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count": 0,
        }
