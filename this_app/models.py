from flask import session, request
from werkzeug.security import generate_password_hash

class User(object):
    """Represents a user who can Create, Read, Update & Delete his own  Shoplists"""

    user_id = 0
    users = {}

    def __init__(self, email, username, password):
        """Constructor to initialize class"""

        User.user_id += 1    # This line is a game changer
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)


    def create_user(self):
        """ Class to create and store a user object """

        self.users.update({
            self.user_id: {
                'email': self.email,
                'username': self.username,
                'password': self.password
            }
        })

        return self.users


class  Shoplist(object):
    """Represents a class to Create, Read, Update & Delete a Shoplist"""

    shop_id = 0
    Shoplists = {}

    def __init__(self, name, description):
        """Constructor to initialize class"""

        Shoplist.shop_id += 1   
        self.name = name
        self.description = description


    def create_shoplist(self):
        """ Class to create and store a  Shoplist object """

        self. Shoplists.update({
            self.shop_id: {'user_id': User.user_id, 'name': self.name, 'description': self.description}
        })

        return self. Shoplists


    def edit_shoplist(self):
        """
        Class to edit  Shoplist
        """
        shoplists_dict =  Shoplist. Shoplists
        for item in shoplists_dict.values():
            if session['user_id'] == item['user_id']:
                for key, val in shoplists_dict.items():
                    if key == int(request.form['key']):
                        print('To be edited =', shoplists_dict[key])
                        existing_owner = val['user_id']
                        shoplists_dict[key] = {'user_id': existing_owner, 'name': self.name, 'description': self.description}

                        return shoplists_dict

    @staticmethod
    def get_all():
        """
        Gets all the  Shoplists created by a logged in user
        """
        print ('User  Shoplists')
        
        all_shoplists =  Shoplist. Shoplists.items()
        user_shoplists = {k:v for k, v in all_shoplists if session['user_id']==v['user_id']}

        return user_shoplists

    @staticmethod
    def delete_shoplist():
        """
        Deletes a single  Shoplist created by a logged in user
        """
        # Retrieve a user's  Shoplist using it's ID
        shoplists_dict =  Shoplist. Shoplists
        for item in shoplists_dict.values():
            if session['user_id'] == item['user_id']:
                for key in shoplists_dict:
                    if key == int(request.form['key']):
                        print('To be deleted =', shoplists_dict[key])
                        del shoplists_dict[key]

                        print('Should have been deleted =', shoplists_dict)

                        return shoplists_dict


class Activity(object):
    """Represents a class to Create, Read, Update & Delete  Shoplist items"""

    activity_id = 0
    activities = {}

    def __init__(self, title, description, status):
        """Constructor to initialize class"""

        Activity.activity_id += 1
        self.title = title
        self.description = description
        self.status = status

    def create_activity(self, shoplist_id):
        """ Class to create and store a  Shoplist item """

        self.activities.update({
            self.activity_id: {
                'shoplist_id': shoplist_id,
                'title': self.title,
                'description': self.description,
                'status': self.status
            }
        })
        
        return self.activities

    def edit_activity(self, shoplist_id, key):
        """
        Class to edit activities
        """
        all_activities = Activity.activities
        for k, val in all_activities.items():
            if k == key and val['shoplist_id'] == shoplist_id:
                print('To be edited =', all_activities[k])
                parent_shoplist = val['shoplist_id']
                all_activities[k] = {'shoplist_id': parent_shoplist, 'title': self.title, 'description': self.description, 'status': self.status}

                print('Should have been edited =', all_activities)

                return all_activities

    @staticmethod
    def get_all():
        """
        Gets all the activities created by a logged in user
        """
        print ('User activities')
        
        all_activities = Activity.activities.items()
        user_activities = {k:v for k, v in all_activities if session['user_id']==v['user_id']}
        # Now get the activities belonging to a particular  Shoplist
        shop_activities = {k:v for k, v in user_activities if session['shoplist_id']==v['shoplist_id']}


        return shop_activities

    @staticmethod
    def delete_activity(shoplist_id, key):
        """
        Deletes a single  Shoplist created by a logged in user
        """
        print('Passing')
        print('Key', key)
        all_activities = Activity.activities
        for item in all_activities.values():
            if shoplist_id == item['shoplist_id']:
                for k in all_activities:
                    if k == key:
                        print('To be deleted =', all_activities[key])
                        del all_activities[key]
                        print('Should have been deleted =', all_activities)

                        return all_activities
