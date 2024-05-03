# API Specification

## Contributors:
- Henry Chen
- Kevin Huang
- Xiaokun Du

Values wrapped in `< >` are placeholders for actual field values.

## Expected Functionality

### Get All Users
- **GET** `/api/users/`
  - **Response** (HTTP STATUS CODE 200)
    ```YAML
    {
        "users": [
            {
                "id": <ID>,
                "name": <USER NAME>,
                "username": <USERNAME>,
                "profile_pic": <PROFILE PIC URL>
            },
            ...
        ]
    }
    ```

### Create a User
- **POST** `/api/users/`
  - **Request**
    ```YAML
    {
        "name": "John Doe",
        "username": "johndoe",
        "profile_pic": "https://example.com/profile.jpg" // Optional
    }
    ```
  - **Response** (HTTP STATUS CODE 201)
    ```YAML
    {
        "id": <ID>,
        "name": "John Doe",
        "username": "johndoe",
        "profile_pic": "https://example.com/profile.jpg"
    }
    ```
  - If name or username is not provided, response (HTTP STATUS CODE 400)
    ```YAML
    {
        "Error": "name or username field not provided"
    }
    ```

### Get User by ID
- **GET** `/api/users/<id>/`
  - **Response** (HTTP STATUS CODE 200)
    ```YAML
    {
        "id": <ID>,
        "name": <USER NAME>,
        "username": <USERNAME>,
        "profile_pic": <PROFILE PIC URL>
    }
    ```
  - If user does not exist, response (HTTP STATUS CODE 404)
    ```YAML
    {
        "Error": "The requested user could not be found"
    }
    ```

### Get User's Posts
- **GET** `/api/users/<id>/posts/`
  - **Response** (HTTP STATUS CODE 200)
    ```YAML
    {
        "Posts": [
            {
                "id": <ID>,
                "title": <POST TITLE>,
                "description": <DESCRIPTION>,
                "image": <IMAGE URL>,
                "meal_type": <MEAL TYPE>,
                "date": <DATE>,
                "user_id": <USER ID>
            },
            ...
        ]
    }
    ```
  - If user does not exist, response (HTTP STATUS CODE 404)
    ```YAML
    {
        "Error": "The requested user could not be found on the server"
    }
    ```

### Add User Saved Post
- **POST** `/api/users/<id>/saved_post/<post_id>/`
  - **Response** (HTTP STATUS CODE 201)
    ```YAML
    {
        "user_id": <USER ID>,
        "post_id": <POST ID>
    }
    ```
  - If user or post does not exist, response (HTTP STATUS CODE 404)
    ```YAML
    {
        "Error": "User or post could not be found on the server"
    }
    ```

### Get User Saved Posts
- **GET** `/api/users/<id>/saved_post/`
  - **Response** (HTTP STATUS CODE 200)
    ```YAML
    {
        "saved_post": [
            {
                "user_id": <USER ID>,
                "post_id": <POST ID>
            },
            ...
        ]
    }
    ```

### Add Meal Plan
- **POST** `/api/mealplan/`
  - **Request**
    ```YAML
    {
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "meal_type": "Breakfast",
        "date": "2022-05-20"
    }
    ```
  - **Response** (HTTP STATUS CODE 201)
    ```YAML
    {
        "id": <MEAL PLAN ID>,
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "type": "Breakfast",
        "date": "2022-05-20"
    }
    ```
  - If any required field is missing, or the user or post does not exist, response (HTTP STATUS CODE 400 or 404 respectively)
    ```YAML
    {
        "Error": "Missing fields for a mealplan" // or "The user or post could not be found on the server"
    }
    ```

### Update Meal Plan
- **POST** `/api/mealplan/<id>/`
  - **Request**
    ```YAML
    {
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "meal_type": "Lunch",
        "date": "2022-05-21"
    }
    ```
  - **Response** (HTTP STATUS CODE 200)
    ```YAML
    {
        "id": <MEAL PLAN ID>,
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "type": "Lunch",
        "date": "2022-05-21"
    }
    ```

### Get User's Meal Plan by ID
- **GET** `/api/mealplan/<id>/`
  - **Response** (HTTP STATUS CODE 200)
    ```YAML
    {
        "id": <MEAL PLAN ID>,
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "type": <MEAL TYPE>,
        "date": <DATE>
    }
    ```
  - If meal plan does not exist, response (HTTP STATUS CODE 404)
    ```YAML
    {
        "Error": "The resource could not be found on the server"
    }
    ```

### Get User's Current Week Meal Plan
- **GET** `/api/users/<id>/mealplan/`
  - **Response** (HTTP STATUS CODE 200)
    ```YAML
    {
        "id": <MEAL PLAN ID>,
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "type": <MEAL TYPE>,
        "date": <DATE>
    }
    ```

### Add Post
- **POST** `/api/posts/`
  - **Request**
    ```YAML
    {
        "title": "Delicious Vegan Burger",
        "description": "A healthy and tasty burger that's completely vegan!",
        "image": "https://example.com/burger.jpg",
        "meal_type": "Dinner",
        "date": "2022-05-22",
        "user_id": <USER ID>
    }
    ```
  - **Response** (HTTP STATUS CODE 201)
    ```YAML
    {
        "id": <POST ID>,
        "title": "Delicious Vegan Burger",
        "description": "A healthy and tasty burger that's completely vegan!",
        "image": "https://example.com/burger.jpg",
        "meal_type": "Dinner",
        "date": "2022-05-22",
        "user_id": <USER ID>
    }
    ```
  - If required fields are missing, response (HTTP STATUS CODE 400)
    ```YAML
    {
        "Error": "Missing required fields for a post"
    }
    ```
