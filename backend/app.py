from db import db
from flask import Flask, request
import json
from db import User
from db import Post
from db import SavedPost
from db import MealPlan

# main.db file should be on the docker image and hosted on the server. 
# Access should not be a public repository for security.
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
    
    all_users=[]

    for user in User.query.all():
        all_users.append(user.serialize())
    
    return success_response({"users": all_users}, 200)

@app.route("/api/users/", methods=["POST"])
def add_user():
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
    
    user=db.session.get(User, id)

    if not user:
        return failure_response({"Error": "The requested user could not be found"}, 404)
    
    return success_response(user.serialize(), 200)

@app.route("/api/users/<id>/posts/", methods=["GET"])
def get_user_posts(id):

    user=db.session.get(User, id)

    if not user:
        return failure_response({"Error":" The requested user could not be found on the server"}, 404)

    all_user_post= Post.query.filter(User.id==id)
    serialized_post=[]
    for post in all_user_post:
        serialized_post.append(post.serialize())
    
    return success_response({"Posts": serialized_post}, 200)

@app.route("/api/users/<id>/saved_post/<post_id>/", methods=["POST"])
def add_user_saved_post(id, post_id):

    user= db.session.get(User, id)
    post= db.session.get(Post, post_id)

    if not user or not post:
        return failure_response({"Error": "User or post could not be found on the server"}, 404)

    new_post= SavedPost(user_id=id, post_id=post_id)
    db.session.add(new_post)
    db.session.commit()

    return success_response(new_post.serialize(), 201)

@app.route("/api/users/<id>/saved_post/", methods=["GET"])
def get_user_saved_post(id):
    
    user_saved_post= SavedPost.query.filter(SavedPost.user_id==id)
    serialized_saved_post=[]
    for post in user_saved_post:
        serialized_saved_post.append(post.serialize())
    
    return success_response({"saved_post": serialized_saved_post}, 200)

@app.route("/api/mealplan/", methods=["POST"])
def add_mealplan():
    
    info=json.loads(request.data)
    user_id= info.get("user_id")
    post_id= info.get("post_id")
    meal_type= info.get("meal_type")
    date= info.get("date")

    field_present= not user_id or not post_id or not meal_type or not date

    if field_present:
        return failure_response({"Error": "Missing fields for a mealplan"}, 400)
    
    user= db.session.get(User, int(user_id))
    post= db.session.get(Post, int(post_id))

    if not user or not post:
        return failure_response({"Error": "The user or post could not be found on the server"}, 404)

    new_mealplan= MealPlan(user_id=user_id, post_id=post_id, type=meal_type, date=date)

    db.session.add(new_mealplan)
    db.session.commit()

    return success_response(new_mealplan.serialize(), 201)

@app.route("/api/mealplan/<id>/", methods=["POST"])
def update_user_mealplan(id):
    
    info= json.loads(request.data)
    user_id= info.get("user_id")
    post_id= info.get("post_id")
    meal_type= info.get("meal_type")
    date= info.get("date")

    fields_present= not user_id or not post_id or not meal_type or not date

    if fields_present:
        return failure_response({"Error": "Missing fields user_id or post_id or meal_type or date"}, 400)
    
    user= db.session.get(User, int(user_id))
    post= db.session.get(Post, int(post_id))

    if not user or not post:
        return failure_response({"Error": "The user or post could not be found on the server"}, 404)
    
    mealplan= MealPlan.query.filter(MealPlan.id==id).first()
    mealplan.user_id= user_id
    mealplan.post_id= post_id
    mealplan.type= meal_type
    mealplan.date= date

    db.session.commit()
    # updated_mealplan= MealPlan.query.filter(MealPlan.id==id).first()
    return success_response(mealplan.serialize(), 200)
    
    

@app.route("/api/users/<id>/mealplan/<meal_id>/")
def get_user_mealplan(id, meal_id):
    pass

@app.route("/api/users/<id>/mealplan/")
def get_user_currweek_mealplan():
    # Use time.now and figure out the start of the week and the end of the week.
    # For a given user find the days in this range and then map from sunday to saturday correctly
    pass

@app.route("/api/posts/", methods=["POST"])
def add_post():
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





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)