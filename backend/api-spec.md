# API Specification

## Contributors:
- Henry Chen
- Kevin Huang
- Xiaokun Du

Values wrapped in `< >` are placeholders for what the field values should be. 

## Expected Functionality

### Get All Users
- **GET** `/api/users/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
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
    ```json
    {
        "name": "John Doe",
        "username": "johndoe",
        "profile_pic": "https://example.com/profile.jpg" // Optional
    }
    ```
  - **Response** (HTTP STATUS CODE 201)
    ```json
    {
        "id": <ID>,
        "name": "John Doe",
        "username": "johndoe",
        "profile_pic": "https://example.com/profile.jpg"
    }
    ```

### Get User by ID
- **GET** `/api/users/<id>/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
    {
        "id": <ID>,
        "name": <USER NAME>,
        "username": <USERNAME>,
        "profile_pic": <PROFILE PIC URL>
    }
    ```

### Get User's Posts
- **GET** `/api/users/<id>/posts/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
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

### Add User Saved Post
- **POST** `/api/users/<id>/saved_post/<post_id>/`
  - **Response** (HTTP STATUS CODE 201)
    ```json
    {
        "user_id": <USER ID>,
        "post_id": <POST ID>
    }
    ```

### Get User Saved Posts
- **GET** `/api/users/<id>/saved_post/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
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
    ```json
    {
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "meal_type": "Breakfast",
        "date": "2022-05-20"
    }
    ```
  - **Response** (HTTP STATUS CODE 201)
    ```json
    {
        "id": <MEAL PLAN ID>,
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "type": "Breakfast",
        "date": "2022-05-20"
    }
    ```

### Update Meal Plan
- **POST** `/api/mealplan/<id>/`
  - **Request**
    ```json
    {
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "meal_type": "Lunch",
        "date": "2022-05-21"
    }
    ```
  - **Response** (HTTP STATUS CODE 200)
    ```json
    {
        "id": <MEAL PLAN ID>,
        "user_id": <USER ID>,
        "post_id": <POST ID>,
        "type": "Lunch",
        "date": "2022-05-21"
    }
    ```
    
### Get User's Meal Plan
- **GET** `/api/users/<id>/mealplan/<meal_id>/`
  - **Response** (HTTP STATUS CODE )
    ```json
    {
        pass
    }
    ```

### Get User's Current Week Meal Plan
- **GET** `/api/users/<id>/mealplan/`
  - **Response** (HTTP STATUS CODE )
    ```json
    {
        pass
    }
    ```


### Add Post
- **POST** `/api/posts/`
  - **Request**
    ```json
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
    ```json
    {
        "id": <POST ID>,
        "title": "Delicious Vegan Burger",
        "description": "A healthy and tasty burger that's completely vegan!",
        "image": "https://example.com/burger.jpg",
        "meal_type": "Dinner",
        "date": "2022-05-22",
        "user_id": "<USER ID>"
    }
    ```
