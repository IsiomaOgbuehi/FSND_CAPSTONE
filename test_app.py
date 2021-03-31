import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Nutritionist, Client, Article, Subscription
from flask import Flask
from app import create_app
from datetime import datetime
import base64
from base64 import b64encode


# This class defines the project test case
class CapstoneTest(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize App
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        self.headers = {'Authorization': 'Bearer {}'.format(
            os.environ.get('JWT_TOKEN'))}

        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after each req
        pass
        # return super().tearDown()

    def test_index(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['val'], 'Halos')

    '''
        TEST FOR NUTRITIONISTS
    '''

    # Test to create Nutritionist
    def test_create_nutritionist(self):
        res = self.client().post('/nutritionists',
                                 json={'name': 'Maskot Rise', 'specialization': 'Pediatrics', 'rating': 0, 'email': 'maskot@test.com'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['email'])

    # Get All Nutritionists
    def test_get_all_nutritionists(self):
        res = self.client().get('/nutritionists',
                                headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    # def test_404_get_all_nutritionists(self):
    #     res = self.client().get('/nutritionists', headers=self.headers)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # Get Specific Nutritionist
    def test_get_specific_nutritionists(self):
        res = self.client().get('/nutritionists/1', headers=self.headers)
        data = json.loads(res.data)
        self.assertTrue(data['data'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_specific_nutritionists(self):
        res = self.client().get('/nutritionists/80', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    # Test to Update Nutritionist
    def test_update_nutritionist(self):
        res = self.client().patch('/nutritionists',
                                  json={'id': 1, 'name': 'Smaklie Brown', 'specialization': 'Pediatrics', 'email': 'smaklie@test.com', 'rating': 5}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_422_update_nutritionist(self):
        res = self.client().patch('/nutritionists',
                                  json={'id': 70, 'name': 'Smallie Brown', 'specialization': 'Pediatrics', 'email': 'smallie@test.com'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    '''
        TEST FOR CLIENTS
    '''

    # Test for creating clients
    def test_create_client(self):
        res = self.client().post('/clients',
                                 json={'name': 'Manning Dreake', 'country': 'Sebean', 'email': 'manning@test'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['email'])

    # Test to Get all Clients
    def test_get_all_clients(self):
        res = self.client().get('/clients', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    # def test_404_get_all_clients(self):
    #     res = self.client().get('/clients', headers=self.headers)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # Test to Get Specific Client
    def test_get_specific_client(self):
        res = self.client().get('/clients/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_404_get_specific_client(self):
        res = self.client().get('/clients/65', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Test to Update Client
    def test_update_client(self):
        res = self.client().patch(
            '/clients', json={'id': 1, 'name': 'Bangas Lukas'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_422_update_client(self):
        res = self.client().patch(
            '/clients', json={'id': 56, 'name': 'Bukky Roadman'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    '''
        TEST FOR ARTICLES
    '''

    # Test for creating articles
    def test_create_article(self):
        res = self.client().post('/articles',
                                 json={'nutritionist': 1, 'title': 'LACTOSE Intolerance', 'date_created':
                                       datetime.now(), 'content': 'Lorem Ipsume Content Alreadiy'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test to get all articles
    def test_get_all_articles(self):
        res = self.client().get('/articles', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])


    # Test get articles based on client subscription
    def test_get_client_articles(self):
        res = self.client().get('/articles?client_id=1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

        
    # Test get articles created by specific nutritionist
    def test_get_nutritionist_articles(self):
        res = self.client().get('/articles?nutritionist_id=8', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])


    # Test to Edit/Update Article
    def test_update_article(self):
        res = self.client().patch('/articles', json={'id': 23, 'title': 'LACTOSE TOLERANCE', 'date_created':
                                                     datetime.now(), 'content': 'Ipsume LOREM Content Delirel'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_422_update_article(self):
        res = self.client().patch('/articles', json={'id': 51, 'title': 'LACTOSE TOLERANCE', 'date_created':
                                                     datetime.now(), 'content': 'Ipsume LOREM Content Delirel'}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test Delete Article
    def test_delete_article(self):
        res = self.client().delete('/articles/24', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_422_delete_article(self):
        res = self.client().delete('/articles/50', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
    # Test to Subscribe
    def test_client_subscription(self):
        res = self.client().post('/subscriptions',
                                 json={'nutritionist_id': 1, 'client_id': 2, 'subscription_status': True}, headers=self.headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
