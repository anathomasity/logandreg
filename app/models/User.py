from system.core.model import Model
import re 

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):
        password = info['password']
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not info['first_name']:
            errors.append('Name cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['last_name']:
            errors.append('Last Name cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Last Name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
    
        if errors:
            return {"status": False, "errors": errors}
        else:
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO `users` (`first_name`, `last_name`, `email`, `password`) VALUES (:first_name, :last_name, :email, :password);"
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'password': hashed_pw
            }
            self.db.query_db(query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }

    def login_user(self, info):

        password = info['password']

        user_query = "SELECT * FROM users WHERE email = :email"
        user_data = {'email': info['email']}

        user = self.db.query_db(user_query, user_data)

        
        if user:
            name = user[0]['first_name']
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                return name
        return False

    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """