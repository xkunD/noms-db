# API Specification

## Contributors:
- Henry Chen
- Kevin Huang
- Xiaokun Du

Values wrapped in `&lt; &gt;` are placeholders for what the field values should be. 

## Expected Functionality

### Get All Users
- **GET** `/api/users/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
    {
        "users": [
            {
                "id": &lt;ID&gt;,
                "name": &lt;USER NAME&gt;,
                "username": &lt;USERNAME&gt;,
                "profile_pic": &lt;PROFILE PIC URL&gt;
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
        "id": &lt;ID&gt;,
        "name": "John Doe",
        "username": "johndoe",
        "profile_pic": "https://example.com/profile.jpg"
    }
    ```

### Get User by ID
- **GET** `/api/users/&lt;id&gt;/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
    {
        "id": &lt;ID&gt;,
        "name": &lt;USER NAME&gt;,
        "username": &lt;USERNAME&gt;,
        "profile_pic": &lt;PROFILE PIC URL&gt;
    }
    ```

### Get User's Posts
- **GET** `/api/users/&lt;id&gt;/posts/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
    {
        "Posts": [
            {
                "id": &lt;ID&gt;,
                "title": &lt;POST TITLE&gt;,
                "description": &lt;DESCRIPTION&gt;,
                "image": &lt;IMAGE URL&gt;,
                "meal_type": &lt;MEAL TYPE&gt;,
                "date": &lt;DATE&gt;,
                "user_id": &lt;USER ID&gt;
            },
            ...
        ]
    }
    ```

### Add User Saved Post
- **POST** `/api/users/&lt;id&gt;/saved_post/&lt;post_id&gt;/`
  - **Response** (HTTP STATUS CODE 201)
    ```json
    {
        "user_id": &lt;USER ID&gt;,
        "post_id": &lt;POST ID&gt;
    }
    ```

### Get User Saved Posts
- **GET** `/api/users/&lt;id&gt;/saved_post/`
  - **Response** (HTTP STATUS CODE 200)
    ```json
    {
        "saved_post": [
            {
                "user_id": &lt;USER ID&gt;,
                "post_id": &lt;POST ID&gt;
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
        "user_id": &lt;USER ID&gt;,
        "post_id": &lt;POST ID&gt;,
        "meal_type": "Breakfast",
        "date": "2022-05-20"
    }
    ```
  - **Response** (HTTP STATUS CODE 201)
    ```json
    {
        "id": &lt;MEAL PLAN ID&gt;,
        "user_id": &lt;USER ID&gt;,
        "post_id": &lt;POST ID&gt;,
        "type": "Breakfast",
        "date": "2022-05-20"
    }
    ```

### Update Meal Plan
- **POST** `/api/mealplan/&lt;id&gt;/`
  - **Request**
    ```json
    {
        "user_id": &lt;USER ID&gt;,
        "post_id": &lt;POST ID&gt;,
        "meal_type": "Lunch",
        "date": "2022-05-21"
    }
    ```
  - **Response** (HTTP STATUS CODE 200)
    ```json
    {
        "id": &lt;MEAL PLAN ID&gt;,
        "user_id": &lt;USER ID&gt;,
        "post_id": &lt;POST ID&gt;,
        "type": "Lunch",
        "date": "2022-05-21"
    }
    ```
    
### Get User's Meal Plan
- **GET** `/api/users/&lt;id&gt;/mealplan/&lt;meal_id&gt;/`
  - **Response** (HTTP STATUS CODE )
    ```json
    {
        pass
    }
    ```

### Get User's Current Week Meal Plan
- **GET** `/api/users/&lt;id&gt;/mealplan/`
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
        "user_id": &lt;USER ID&gt;
    }
    ```
  - **Response** (HTTP STATUS CODE 201)
    ```json
    {
        "id": &lt;POST ID&gt;,
        "title": "Delicious Vegan Burger",
        "description": "A healthy and tasty burger that's completely vegan!",
        "image": "https://example.com/burger.jpg",
        "meal_type": "Dinner",
        "date": "2022-05-22",
        "user_id": &lt;USER ID&gt;
    }
    ```
