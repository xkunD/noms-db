from db import db
from flask import Flask, request
import json
from db import User
from db import Post
from db import SavedPost
from db import MealPlan
import datetime

app = Flask(__name__)
db_filename = "main.db"
BLANK_PROFILE_URL="https://ibb.co/fqjBRDL"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

def success_response(data,code=200):
    """
        General success response for a request.

        Parameters
        -----------
        data: any
            Json formattable data.
        code: int
            HTTP response code
        
        Return 
        -----------
        json: JSON
            Response in json format
    """
    
    return json.dumps(data), code

def failure_response(err_message,code=404):
    """
        General failure response for a request.

        Parameters
        ------------
        data: any
            Json formattable data.
        code: int
            HTTP response code.

        Return 
        -----------
        json: JSON
            Response in json format

    """
    
    return json.dumps(err_message), code

@app.route("/api/users/", methods=["GET"])
def get_all_users():
    """
        Retrieves all users.

        Returns
        ------------

        json: JSON
            HTTP Response with information on all users.
    """
    
    all_users=[]

    for user in User.query.all():
        all_users.append(user.serialize())
    
    return success_response({"users": all_users}, 200)

@app.route("/api/users/", methods=["POST"])
def add_user():
    """
        Add a user

        Returns
        -----------

        json: JSON
            Http response with the information of the added user.
    """
    info= json.loads(request.data)
    name= info.get("name")
    username= info.get("username")
    profile_pic= info.get("profile_pic", BLANK_PROFILE_URL)

    if not name or not username:
        return failure_response({"Error": "name or username field not provided"}, 400)

    new_user= User(name=name, username=username, profile_pic=profile_pic)

    db.session.add(new_user)

    db.session.commit()

    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<id>/", methods=["GET"])
def get_user_by_id(id):
    """
        Retrieve the user with id, id

        Parameters
        --------------
        id: int
            id of the user to retrieve.

        Returns
        --------------
        json: JSON
            HTTP response with information on the user with id, id.
    """
    
    user=db.session.get(User, id)

    if not user:
        return failure_response({"Error": "The requested user could not be found"}, 404)
    
    return success_response(user.serialize(), 200)

@app.route("/api/users/<id>/posts/", methods=["GET"])
def get_user_posts(id):
    """
        Retrieves all post made by the user with id, id.

        Parameters
        --------------
        id: int
            Id of the users to retrieve post for.
        
        Return
        --------------
        json: JSON
            HTTP response with the posts made by user with id, id.
    """

    user=db.session.get(User, id)

    if not user:
        return failure_response({"Error":" The requested user could not be found on the server"}, 404)

    all_user_post= Post.query.filter(User.id==id)
    serialized_post=[]
    for post in all_user_post:
        serialized_post.append(post.serialize())
    
    return success_response({"Posts": serialized_post}, 200)

@app.route("/api/users/<id>/saved_post/", methods=["POST"])
def add_user_saved_post(id):
    """
        Add a post to the saved post for the user with id, id.

        Parameter
        ------------
        id: int
            Id of the user to save a post for
        
        Return
        ------------
        json: JSON
            HTTP response specifying user with id, id saving post with a given post id.
    """

    info= json.loads(request.data)
    post_id= info.get("post_id")

    if post_id==None:
        return failure_response({"Error": "Missing post_id field"}, 400)

    user= db.session.get(User, id)
    post= db.session.get(Post, int(post_id))

    if not user or not post:
        return failure_response({"Error": "User or post could not be found on the server"}, 404)

    new_post= SavedPost(user_id=id, post_id=post_id)
    db.session.add(new_post)
    db.session.commit()

    return success_response(new_post.serialize(), 201)

@app.route("/api/users/<id>/saved_post/", methods=["GET"])
def get_user_saved_post(id):
    """
        Retrieve all the saved post associated with the user with id, id.

        Parameters
        -------------
        id:int
            Id of the user 
        
        Returns
        -------------
        json: JSON
            HTTP response with all the post user with id, id saved.
    """
    
    user_saved_post= SavedPost.query.filter(SavedPost.user_id==id)
    serialized_saved_post=[]
    for post in user_saved_post:
        serialized_saved_post.append(post.serialize())
    
    return success_response({"saved_post": serialized_saved_post}, 200)

@app.route("/api/mealplan/", methods=["POST"])
def add_mealplan():
    """
        Add a mealplan 

        Returns
        ----------
        json: JSON
            HTTP response with information on the added mealplan.
    """
    
    info=json.loads(request.data)
    user_id= info.get("user_id")
    breakfast_id= info.get("breakfast_id")
    lunch_id= info.get("lunch_id")
    dinner_id= info.get("dinner_id")
    date= info.get("date")

    meals=[breakfast_id, lunch_id, dinner_id]
    one_valid_id= False
    for id in meals:
        if id is not None:
            one_valid_id=True

    field_unpresent= not user_id or not date or not one_valid_id

    if field_unpresent:
        return failure_response({"Error": "Missing fields for a mealplan"}, 400)
    
    
    user= db.session.get(User, int(user_id))
    valid= True
    for id in meals:
        if id is not None:
            post_info= db.session.get(Post, int(id))
            if not post_info:
                valid=False
    

    if not user or not valid:
        return failure_response({"Error": "The user could not be found or a post could not found for the meal."}, 404)

    new_mealplan= MealPlan(user_id=user_id, breakfast_id=breakfast_id, lunch_id=lunch_id, dinner_id=dinner_id, date=date)

    db.session.add(new_mealplan)
    db.session.commit()

    return success_response(new_mealplan.serialize(), 201)

@app.route("/api/mealplan/<id>/", methods=["POST"])
def update_user_mealplan(id):
    """
        Update the mealplan with id, id

        Parameters
        ------------
        id: int
            Id of the mealplan to update
        
        Returns
        ------------
        json: JSON
            HTTP response with the updated information for the mealplan with id, id
    """
    
    info=json.loads(request.data)
    breakfast_id= info.get("breakfast_id")
    lunch_id= info.get("lunch_id")
    dinner_id= info.get("dinner_id")
    date= info.get("date")

    meals=[breakfast_id, lunch_id, dinner_id]
    one_valid_id= False
    for id in meals:
        if id is not None:
            one_valid_id=True

    field_unpresent= not date or not one_valid_id

    if field_unpresent:
        return failure_response({"Error": "Missing fields to update a mealplan"}, 400)
    
    valid= True
    for id in meals:
        if id is not None:
            post_info= db.session.get(Post, int(id))
            if not post_info:
                valid=False

    if not valid:
        return failure_response({"Error": "A post could not be found for the meal."}, 404)

    mealplan= MealPlan.query.filter(MealPlan.id==id).first()
    mealplan.breakfast_id= breakfast_id
    mealplan.lunch_id= lunch_id
    mealplan.dinner_id= dinner_id
    mealplan.date= date

    db.session.commit()
    return success_response(mealplan.serialize(), 200)
    
@app.route("/api/mealplan/<id>/", methods=["GET"])
def get_mealplan(id):
    """
        Retrieve the mealplan with id, id

        Parameters
        -------------
        id: int
            id of the mealplan to retrieve
        
        Returns
        -------------
        json: JSON
            HTTP response with the information of the mealplan with id, id.
    """
    
    mealplan= MealPlan.query.filter(MealPlan.id==id).first()

    if not mealplan:
        return failure_response({"Error": "The resource could not be found on the server"}, 404)
    
    return success_response(mealplan.serialize(), 200)

@app.route("/api/users/<id>/mealplan/", methods=["GET"])
def get_user_currweek_mealplan(id):
    """
        Retrieves the mealplan for the current week

        Parameters
        -------------
        id: int
            User id
        
        Returns
        -------------
        json: JSON
            HTTP response with the mealplans for the user for the current week.
    """
    
    today= datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday()+1)
    end_of_week = start_of_week + datetime.timedelta(days=6)
    week_range = []
    for day in range((end_of_week - start_of_week).days + 1):
        date = start_of_week + datetime.timedelta(days=day)
        week_range.append(date.strftime("%m/%d/%y"))
    
    currweek_mealplan=[]
    for date in week_range:
        # Can only be one result but structure for app is weird.
        mealplan= MealPlan.query.filter(db.and_(MealPlan.user_id==id, MealPlan.date==date)).first()
        if not mealplan:
            currweek_mealplan.append(None)
        else:
            currweek_mealplan.append(mealplan.serialize())
    
    return success_response(currweek_mealplan, 200)

@app.route("/api/posts/", methods=["POST"])
def add_post():
    """
        Add a post

        Returns
        ----------
        json: JSON
            HTTP response with information on the added post.
    """
    info=json.loads(request.data)
    title= info.get("title")
    description= info.get("description")
    image= info.get("image")
    meal_type= info.get("meal_type")
    date= info.get("date")
    user_id= info.get("user_id")

    fields_present= not info or not title or not description or not image or not meal_type or not date or not user_id

    if fields_present:
        return failure_response({"Error":"Missing required fields for a post"}, 400)
    
    new_post= Post(title=title, description=description, image=image, meal_type=meal_type, date=date, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return success_response(new_post.serialize(), 201)

@app.route("/api/posts/", methods=["GET"])
def get_all_post():
    """
        Retrieve all posts

        Returns
        -----------
        json: JSON
            HTTP response with information on all posts.
    """
    all_post=[]

    for post in Post.query.all():
        all_post.append(post.serialize())
    
    return success_response({"posts": all_post}, 200)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)