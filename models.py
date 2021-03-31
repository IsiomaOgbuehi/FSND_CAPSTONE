import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from sqlalchemy.sql import func

database_name = "capstone"
# database_path = "postgresql://{}/{}".format(
#     'postgres:root@localhost:5432', database_name)
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()

'''
    NUTRITIONIST MODEL
'''
class Nutritionist(db.Model):
    __tablename__ = 'nutritionists'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    specialization = db.Column(String(100), nullable=False)
    rating = db.Column(Integer, default=0)
    email = db.Column(String(100), nullable=False)
    subscriptions = db.relationship(
        'Subscription', backref='subscription_nutritionist', lazy=True)
    articles = db.relationship(
        'Article', backref='article_nutritionist', lazy=True)

    def __init__(self, name, specialization, rating, email):
        self.name = name
        self.specialization = specialization
        self.rating = rating
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'rating': self.rating,
            'email': self.email
        }


'''
    CLIENT MODEL
'''
class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    country = db.Column(String(100), nullable=False)
    email = db.Column(String(100), nullable=False)
    subscriptions = db.relationship(
        'Subscription', backref='client_nutritionist', lazy=True)

    def __init__(self, name, country, email):
        self.name = name
        self.country = country
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'name': self.name,
            'country': self.country,
            'email': self.email
        }


'''
    ARTICLE MODEL
'''


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = Column(DateTime(timezone=True),
                          default=func.now(), onupdate=func.now())
    content = db.Column(db.Text, nullable=False)
    nutritionist_id = db.Column(Integer, db.ForeignKey(
        'nutritionists.id'), nullable=False)

    def __init__(self, title, date_created, content, nutritionist):
        self.title = title
        self.date_created = date_created
        self.content = content
        self.nutritionist = nutritionist

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'title': self.title,
            'date_created': self.date_created,
            'content': self.content
        }


'''
    SUBSCRIPTION MODEL
'''
class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(Integer, primary_key=True)
    nutritionist_id = db.Column(Integer, db.ForeignKey('nutritionists.id'), nullable=False)
    client_id = db.Column(Integer, db.ForeignKey('clients.id'), nullable=False)
    subscription_status = db.Column(db.Boolean, nullable=False, default=True)
    
    def __init__(self, nutritionist_id, client_id, subscription_status):
        self.nutritionist_id = nutritionist_id
        self.client_id = client_id
        self.subscription_status = subscription_status
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'nutritionist_id': self.nutritionist_id,
            'client_id': self.client_id,
            'subscription_status': self.subscription_status
        }
    
