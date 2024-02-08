import requests
import pytest

base_url = "https://petstore.swagger.io/v2"

@pytest.fixture(scope="module")
def user_credentials():
    return {
        "username": "Likeuser",
        "password": "LikePassword"
    }

def test_create_user():
    # Step Description: Create a new user by sending a POST request to the user creation endpoint.
    endpoint = f"{base_url}/user"
    user_data = {
        "id": 77,
        "username": "Likeuser",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser@example.com",
        "password": "testPassword",
        "phone": "1234567890"
    }
    response = requests.post(endpoint, json=user_data)
    assert response.status_code == 200
    assert response.json()["code"] == 200

def test_login_user(user_credentials):
    # Step Description: Log in as a user by sending a GET request to the login endpoint.
    endpoint = f"{base_url}/user/login"
    response = requests.get(endpoint, params=user_credentials)
    assert response.status_code == 200
    assert response.json()["code"] == 200

def test_create_list_of_users():
    # Step Description: Create a list of users by sending a POST request to the user creation with list endpoint.
    endpoint = f"{base_url}/user/createWithList"
    user_data_list = [
        {
            "id": 77,
            "username": "testuser1",
            "firstName": "Test1",
            "lastName": "User1",
            "email": "testuser1@example.com",
            "password": "testPassword1",
            "phone": "1234567891"
        },
        {
            "id": 14,
            "username": "testuser2",
            "firstName": "Test2",
            "lastName": "User2",
            "email": "testuser2@example.com",
            "password": "testPassword2",
            "phone": "1234567892"
        }
    ]
    response = requests.post(endpoint, json=user_data_list)
    assert response.status_code == 200
    assert response.json()["code"] == 200

def test_logout_user(user_credentials):
    # Step Description: Log out the user by sending a POST request to the logout endpoint.
    endpoint = f"{base_url}/user/logout"
    response = requests.get(endpoint, params=user_credentials)
    assert response.status_code == 200

def test_add_new_pet():
    # Step Description: Add a new pet by sending a POST request to the pet creation endpoint.
    endpoint = f"{base_url}/pet"
    pet_data = {
        "id": 77,
        "name": "Fluffy",
        "status": "available"
    }
    response = requests.post(endpoint, json=pet_data)
    assert response.status_code == 200


def test_update_pet_image():
    # Step Description: Update the image of a pet by sending a POST request to the pet update endpoint.
    # Assuming pet ID 1 exists
    pet_id = 77
    endpoint = f"{base_url}/pet/{pet_id}"
    image_url = "https://example.com/new_image.jpg"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(endpoint, data={"image": image_url}, headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 200

def test_update_pet_name_and_status():
    # Step Description: Update the name and status of a pet by sending a PUT request to the pet update endpoint.
    # Assuming pet ID 1 exists
    pet_id = 77
    endpoint = f"{base_url}/pet/{pet_id}"
    updated_data = {
        "name": "Butler",
        "status": "Sale"
    }
    response = requests.get(endpoint, json=updated_data)
    assert response.status_code == 200


def test_delete_pet():
    # Step Description: Delete a pet by sending a DELETE request to the pet deletion endpoint.
    # Assuming pet ID 1 exists
    pet_id = 77
    endpoint = f"{base_url}/pet/{pet_id}"
    response = requests.delete(endpoint)
    assert response.status_code == 200
    assert response.json()["code"] == 200
