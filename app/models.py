from sqlalchemy.orm import backref
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

#assistant table that help build up fans' many-to-many scheme
followers = db.Table("followers",
                     db.Column("follower_id", db.Integer,db.ForeignKey("user.id")),
                     db.Column("followed_id", db.Integer, db.ForeignKey("user.id")))
# define user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # encrypted password
    # represent relationship between user and post:one to multiple
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # set up many-to-many relationship with followers table
    followed = db.relationship("User",secondary=followers, primaryjoin=(followers.c.follower_id==id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref("followers",lazy="dynamic"), lazy="dynamic")
    def __repr__(self):
        return "<User {}>".format(self.username)
    # set up password and encrypt it with hash function

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # use Gravatar service to generate head protrait for each user

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    #return posts of all following users
    def followed_posts(self):
        #following statement will be mapped to SQL query
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
        

# define post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # id in user model should be foreignKey of post model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post {}>".format(self.body)



# when log user in, load that user instance into session
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


