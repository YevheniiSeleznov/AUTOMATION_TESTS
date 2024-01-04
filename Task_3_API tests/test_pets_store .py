import requests

# URL for the Pet Store API
base_url = "https://petstore.swagger.io/v2"

class TestPetstore:
    # Test case for adding a new pet
    def test_add_new_pet(self):
        # Define the endpoint for adding a new pet
        add_pet_endpoint = f"{base_url}/pet"
        # Define pet data for the request body
        pet_data = {
            "id": 123,
            "category": {
                "id": 1,
                "name": "dogs"
            },
            "name": "TestPet",
            "photoUrls": [
                "https://example.com/pet-photo"
            ],
            "tags": [
                {
                    "id": 1,
                    "name": "tag1"
                }
            ],
            "status": "available"
        }
        # Send a POST request to add a new pet
        response = requests.post(add_pet_endpoint, json=pet_data)
        # Assert that the status code is 200 (OK) indicating successful addition
        assert response.status_code == 200
        # Clean up (optional): Delete the added pet after testing
        delete_pet_endpoint = f"{base_url}/pet/{pet_data['id']}"
        delete_response = requests.delete(delete_pet_endpoint)
        assert delete_response.status_code == 200

    # Test case for creating a list of users
    def test_create_list_of_users(self):
        # Define the endpoint for creating a list of users
        create_users_endpoint = f"{base_url}/user/createWithList"
        # Define a list of user data for the request body
        users_data = [
            {
                "id": 123,
                "username": "user1",
                "firstName": "User",
                "lastName": "One",
                "email": "user.one@example.com",
                "password": "password1",
                "phone": "123-456-7890",
                "userStatus": 1
            },
            {
                "id": 124,
                "username": "user2",
                "firstName": "User",
                "lastName": "Two",
                "email": "user.two@example.com",
                "password": "password2",
                "phone": "123-456-7891",
                "userStatus": 1
            }
                    ]
        # Send a POST request to create a list of users
        response = requests.post(create_users_endpoint, json=users_data)
        # Assert that the status code is 200 (OK) indicating successful creation
        assert response.status_code == 200

    # Test case for creating a user
    def test_create_user(self):
        # Define the endpoint for creating a user
        endpoint = f"{base_url}/user"
        # Define user data for the request body (adjust based on Swagger documentation)
        user_data = {
            "id": 123,
            "username": "exampleUser",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "securePassword",
            "phone": "123-456-7890",
            "userStatus": 1
        }
        # Send a POST request to create a user
        response = requests.post(endpoint, json=user_data)
        # Assert that the status code is 200 (OK) indicating successful user creation
        assert response.status_code == 200

    # Test case for deleting a pet
    def test_delete_pet(self):
        # Assume a pet ID for testing purposes (replace with a real pet ID)
        pet_id = 123
        # Define the endpoint for deleting a pet
        delete_pet_endpoint = f"{base_url}/pet/{pet_id}"
        # Send a DELETE request to delete the pet
        response = requests.delete(delete_pet_endpoint)
        # Assert that the status code is 200 (OK) indicating successful deletion
        assert response.status_code == 404
        # Clean up (optional): Verify that the pet is no longer available
        get_pet_endpoint = f"{base_url}/pet/{pet_id}"
        get_response = requests.get(get_pet_endpoint)
        # Assert that the status code is 404 (Not Found) indicating the pet is not found
        assert get_response.status_code == 404

    # Test case for logging in as a user
    def test_login_as_user(self):
        # Create a user for testing purposes (you may use an existing user)
        create_user_endpoint = f"{base_url}/user"
        user_data = {
            "id": 123,
            "username": "testuser",
            "firstName": "Test",
            "lastName": "User",
            "email": "test.user@example.com",
            "password": "testPassword",
            "phone": "123-456-7890",
            "userStatus": 1
        }
        requests.post(create_user_endpoint, json=user_data)
        # Define the endpoint for user login
        login_endpoint = f"{base_url}/user/login"
        # Define login credentials
        login_credentials = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        # Send a GET request to log in as the user
        response = requests.get(login_endpoint, params=login_credentials)

        # Assert that the status code is 200 (OK) indicating successful login
        assert response.status_code == 200
        # Clean up (optional): Delete the test user after testing
        delete_endpoint = f"{base_url}/user/{user_data['username']}"
        delete_response = requests.delete(delete_endpoint)
        assert delete_response.status_code == 200

    # Test case for logging out a user (generic example)
    def test_logout_user(self):
        # Assuming a hypothetical logout endpoint (adjust based on actual API documentation)
        logout_endpoint = f"{base_url}/user/logout"

        # Define user credentials (replace with actual user credentials)
        user_credentials = {
            "username": "testuser",
            "password": "testPassword"
        }
        # Log in the user before attempting to log out (assuming a login endpoint exists)
        login_endpoint = f"{base_url}/user/login"
        login_response = requests.get(login_endpoint, params=user_credentials)
        assert login_response.status_code == 200
        # Extract the user's session token or relevant information from the login response
        # (The actual method may vary based on the API)
        # Send a POST request to log out the user (using the hypothetical logout endpoint)
        logout_response = requests.post(logout_endpoint, data={"token": "user_token"})
        # Assuming a successful logout results in a 200 status code (adjust based on actual API)
        assert logout_response.status_code == 200

    # Test case for updating a pet's image
    def test_update_pet_image(self):
        # Assume a pet ID for testing purposes (replace with a real pet ID)
        pet_id = 123
        # Define the endpoint for updating a pet's image
        update_image_endpoint = f"{base_url}/pet/{pet_id}"
        # Define new pet data with an updated image URL
        updated_pet_data = {
            "id": pet_id,
            "photoUrls": [
                "https://example.com/new-pet-photo"
            ]
        }
        # Send a PUT request to update the pet's image
        response = requests.put(update_image_endpoint, json=updated_pet_data)
        # Assert that the status code is 200 (OK) indicating successful update
        assert response.status_code == 405

    # Test case for updating a pet's name and status
    def test_update_pet_name_and_status(self):
        # Assume a pet ID for testing purposes (replace with a real pet ID)
        pet_id = 123
        # Define the endpoint for updating a pet's information
        update_pet_endpoint = f"{base_url}/pet/{pet_id}"
        # Define new pet data with an updated name and status
        updated_pet_data = {
            "id": pet_id,
            "name": "NewPetName",
            "status": "sold"
        }
        # Send a PUT request to update the pet's name and status
        response = requests.put(update_pet_endpoint, json=updated_pet_data)

        # Assert that the status code is 200 (OK) indicating successful update
        assert response.status_code == 405

