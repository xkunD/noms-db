from flask_sqlalchemy import SQLAlchemy

# Default metadata object will be used after since no metadata variable is supplied initially
db = SQLAlchemy()

class User(db.Model):
    """
        ORM model for Users.
    """

    __tablename__= "user"
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username= db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String)
    posts = db.relationship('Post', backref='user', lazy=True)
    saved_posts = db.relationship('Post', secondary='saved_posts', lazy='subquery',
                                  backref=db.backref('saved_by', lazy=True))
    def __init__(self, **kwargs):
        self.name= kwargs.get("name")
        self.username= kwargs.get("username")
        self.profile_pic= kwargs.get("profile_pic")
    
    def serialize(self):
        """
            Serialize user object to be JSON compatible.

            Returns
            ----------
            dict: dict
                Dict with the fields of the user.
        """
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'profile_pic': self.profile_pic
        }


class Post(db.Model):
    """
        ORM model for a Post.
    """

    __tablename__="post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    meal_type = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __init__(self, **kwargs):
        self.title= kwargs.get("title")
        self.description= kwargs.get("description")
        self.image= kwargs.get("image")
        self.meal_type= kwargs.get("meal_type")
        self.date= kwargs.get("date")       
        self.user_id= kwargs.get("user_id")
    
    def serialize(self):
        """
            Serialize the post object to be JSON compatible.

            Returns
            -----------
            dict: dict
                Dict with the fields of the post.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'meal_type': self.meal_type,
            'date': self.date,
            'user_id': self.user_id,
        }

class SavedPost(db.Model):
    """
        ORM model for saved posts.
    """
    __tablename__ = 'saved_posts'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)

    def __init__(self, **kwargs):
        self.user_id= kwargs.get("user_id")
        self.post_id= kwargs.get("post_id")
    
    def serialize(self):
        """
            Serialize a savedpost to be JSON compatible.

            Returns
            -----------
            dict: dict
                dict with the fields of a saved post.
        """
        return {
            "user_id": self.user_id,
            "post_id": self.post_id
        }

class MealPlan(db.Model):
    """
        ORM model for meal plan.
    """
    __tablename__ = 'meal_plans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    breakfast_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    lunch_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    dinner_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    date = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.user_id= kwargs.get("user_id")
        self.breakfast_id= kwargs.get("breakfast_id")
        self.lunch_id= kwargs.get("lunch_id")
        self.dinner_id= kwargs.get("dinner_id")
        self.date= kwargs.get("date")

    def serialize(self):
        """
            Serialize mealplan to be json compatible.

            Returns
            ------------
            dict: dict
                dict containing the fields of a mealplan.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            "breakfast_id": self.breakfast_id,
            "lunch_id": self.lunch_id,
            "dinner_id": self.dinner_id,
            'date': self.date
        }
