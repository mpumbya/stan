from flask import url_for, session
from this_app import app
from this_app.models import User, Shoppinglist, Activity
import unittest


class BasicTestCase(unittest.TestCase):
    """ Basic flask setup tests """

    def test_index(self):
        """ Initial test to ensure flask was setup correctly """
        tester = app.test_client(self)        # You can use self.app in place of tester
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_homepage(self):
        """ Ensure logout redirects to hp """
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_to_shoplists(self):
        """ Ensure signup redirects to login """
        tester = app.test_client(self)
        response = tester.post('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class UserTestCase(unittest.TestCase):
    """ Test the User class """

    def setUp(self):
        """ Setup a new user """
        User.users = {}
        self.app = User('demo@email.com', 'admin', 'admin')
        # Set some default user data
        self.user_data = {
            1: {
                'email': 'demo@email.com',
                'username': 'admin',
                'password': 'admin'  
            }
            
        }

    def test_users_dictionary(self):
        """Test user's dict is empty at first"""
        new_user = self.app
        self.assertEqual(len(new_user.users), 0)
        new_user.create_user()
        self.assertIsInstance(new_user, User)
        self.assertEqual(len(new_user.users), 1)

    def test_user_id(self):
        """Test user_id starts from one and increments by one"""
        new_user = self.app
        self.assertTrue(new_user.user_id, 0)
        new_user.create_user()
        self.assertTrue(new_user.user_id, 1)
        for key in new_user.users:
            self.assertEqual(new_user.user_id, key)

    def test_users_can_signup(self):
        """Test new user can sign up successfully"""
        for value in self.app.users.values():
            result = self.app.create_user()
            stored_password = value['password']
            expected = {0: {
                'email': 'demo@email.com', 'username': 'admin', 'password': stored_password
                }}
            self.assertEqual(expected, result)

    def test_registering_user(self):
        """Test that a user cannot be registered twice."""
        new_user = self.app
        new_user.create_user()
        client = app.test_client(self)
        response = client.post('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Test registered user can login successfully"""
        pass

    def test_invalid_credentials_redirects_to_login(self):
        """Users need valid credentials"""
        tester = app.test_client(self)
        response = tester.post('/login',
                            data=dict(email='demo@email.com',
                                      password='admin'),
                            follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_signup_existing_user_redirects_to_login(self):
        """Users get redirected to login if they have a/c"""
        tester = app.test_client(self)
        response = tester.post('/signup',
                            data=dict(email='demo@email.com',
                                      usrname='admin',
                                      password='admin'),
                            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_shoplists_without_login_redirects(self):
        """Users need valid credentials"""
        tester = app.test_client(self)
        response = tester.post('/show_bucketlists', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_shoplists_dashboard_without_login_redirects(self):
        """Users need valid credentials"""
        tester = app.test_client(self)
        response = tester.get('/show_shoplists', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        del self.app
        del self.user_data


class ShoppinglistTestCase(unittest.TestCase):
    """ Test the Shoppinglist class """

    def setUp(self):
        """ Setup a Shoppinglist """
        User.users = {1: {'demo@email.com', 'admin', 'admin'}}
        self.app = Shoppinglist('Apples', 'Fresh Green apples')
        Shoppinglist.shoplists = {}
        self.client = app.test_client(self)
        # Set some default shopping data
        self.shoplist_data = {
            1: {
                'user_id': 1,
                'name': 'Apples',
                'description': 'Fresh Green apples'
            }
            
        }

    def test_shoplists_dictionary(self):
        """Test Shoppinglist's dict is empty at first"""
        new_shoplist = self.app
        self.assertEqual(len(new_shoplist.shoplists), 0)
        new_shoplist.create_shoplist()
        self.assertIsInstance(new_shoplist, Shoppinglist)
        self.assertEqual(len(new_shoplist.shoplists), 1)

    def test_shoplist_id(self):
        """Test shoplist_id starts from one and increments by one"""
        new_shoplist = self.app
        self.assertTrue(new_shoplist.shop_id, 0)
        new_shoplist.create_shoplist()
        self.assertTrue(new_shoplist.shop_id, 1)
        for key in new_shoplist.shoplists:
            self.assertEqual(new_shoplist.shop_id, key)

    def test_create_shoplist(self):
        """Test shoplist can be created"""
        new_shoplist = self.app
        new_shoplist.create_shoplist()
        self.assertEqual(len(new_shoplist.shoplists), 1)

    def test_user_id_in_shoplist(self):
        """User id starts from one onwards"""
        new_shoplist = self.app
        new_shoplist.create_shoplist()
        for value in Shoppinglist.shoplists.values():
            for key in User.users:
                self.assertEqual(value['user_id']+1, key)
        new_shoplist.create_shoplist()
        for value in Shoppinglist.shoplists.values():
            for key in User.users:
                self.assertEqual(value['user_id']+1, key)

    def test_create_shoplist_without_user_fails(self):
        """Test Shoppinglist creation without a user fails"""
        User.users = {}
        result = self.app.create_shoplist()
        expected = {1: {'user_id': 1, 'name': 'Apple', 'description': 'Fresh Green Apples'}}
        self.assertNotEqual(expected, result)

    def test_successful_shoplist_creation(self):
        """Test Shoppinglist creation is successful"""
        result = self.app.create_shoplist()
        expected = {5: {'user_id': 0, 'name': 'apples', 'description': 'Fresh Green Apples'}}
        self.assertEqual(expected, result)

    def tearDown(self):
        del self.app
        del self.shoplist_data
        del Shoppinglist.shoplists
        del User.users


class ActivityTestCase(unittest.TestCase):
    """ Test the ShoppinglistItem class """

    def setUp(self):
        """ Setup an activity """
        User.users = {1: {'demo@email.com', 'admin', 'admin'}}
        Shoppinglist.shoplists = {1: {'user_id': 1, 'name': 'apples', 'description': 'Fresh Green Apples'}}
        Activity.activities = {}
        self.app = Activity('apples', 'Fresh Green Apples', True)
        # Set some default activity data
        self.activity_data = {
            1: {
                'bucketlist_id': 1,
                'name': 'apples',
                'description': 'Fresh Green Apples',
                'status': True
            }   
        }

    def test_activity_dictionary(self):
        """Test activity's dict is empty at first"""
        new_activity = self.app
        self.assertEqual(len(new_activity.activities), 0)
        new_activity.create_activity(1)
        self.assertIsInstance(new_activity, Activity)
        self.assertEqual(len(new_activity.activities), 1)

    def test_activity_id(self):
        """Test activity_id starts from one and increments by one"""
        new_activity = self.app
        self.assertTrue(Activity.activity_id, 0)
        new_activity.create_activity(1)
        self.assertTrue(new_activity.activity_id, 1)
        for key in new_activity.activities:
            self.assertEqual(new_activity.activity_id, key)

    def test_successful_activity_creation(self):
        """Test Shoppinglist item creation is successful"""
        result = self.app.create_activity(1)
        expected = {4: {'shoplist_id': 1, 'title': 'apples', 'description': 'Fresh Green Apples', 'status': True}}
        self.assertEqual(expected, result)

    def test_show_activities_without_login_redirects(self):
        """Users need valid credentials"""
        User.users = {}
        tester = app.test_client(self)
        response = tester.post('/show_shoplists', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        del self.app
        del self.activity_data
        del Activity.activities
        del Shoppinglist.shoplists
        del User.users
