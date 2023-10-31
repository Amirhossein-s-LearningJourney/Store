from store.models import Collection, Product
from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker
from django.test import TestCase


@pytest.fixture
def creat_collection(api_client):
    # if we pass collection inside the create collection args it will be considered to be a fixture
    # to solve this we use an inner function
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)

    return do_create_collection


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post("/store/products/", product)

    return do_create_product


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


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({"title": "Test Product"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):
        authenticate()
        response = create_product({"title": "Test Product"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)
        response = create_product({"title": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    # def test_if_data_is_valid_returns_201(self, authenticate, create_product):
    #     # Authenticate as a staff member
    #     authenticate(is_staff=True)

    #     # Create a valid product data
    #     data = {
    #         "title": "Test Product",
    #         "slug": "test-product",
    #         "unit_price": 20,
    #         "inventory": 10,
    #         "collection": baker.make(Collection),
    #     }

    #     # Create the product using the create_product fixture
    #     response = create_product(product=data)

    #     # Assert that the response status code is 201
    #     assert response.status_code == status.HTTP_201_CREATE


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self, api_client):
        # Arrange
        product = baker.make(Product)

        response = api_client.get(f"/store/products/{product.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == product.id
        assert response.data["title"] == product.title
