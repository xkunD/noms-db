from flask_sqlalchemy import SQLAlchemy

# Default metadata object will be used after since no metadata variable is supplied initially
db = SQLAlchemy()

class User(db.Model):
    """
        ORM model for Users
    """

    __tablename__= "user"
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    saved_posts = db.relationship('Post', secondary='saved_posts', lazy='subquery',
                                  backref=db.backref('saved_by', lazy=True))
    def __init__(self, **kwargs):
        self.name= kwargs.get("username")
        self.profile_pic= kwargs.get("profile_pic")
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'profile_pic': self.profile_pic(db.String, nullable=False)
        }


class Post(db.Model):
    """
        ORM model for a Post
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
        ORM model for saved posts
    """
    __tablename__ = 'saved_posts'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)


class MealPlan(db.Model):
    """
        ORM model for meal plan
    """
    __tablename__ = 'meal_plans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    type = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'type': self.type,
            'date': self.date
        }
